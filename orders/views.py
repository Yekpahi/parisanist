import json
from django.urls import reverse
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import datetime
from django.shortcuts import render, redirect
import stripe
from carts.models import CartItem
from store.models import Product
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.product_price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.product_stock -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_received_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.product_price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (20 * total) / 100
    grand_total = round((total + tax), 2)

    if request.method == 'POST':
        orderform = OrderForm(request.POST)
        if orderform.is_valid():
            # data = Order()
            data = orderform.save(commit=False)
            data.user = current_user
            data.first_name = orderform.cleaned_data['first_name']
            data.last_name = orderform.cleaned_data['last_name']
            data.zip_code = orderform.cleaned_data['zip_code']
            data.phone = orderform.cleaned_data['phone']
            data.email = orderform.cleaned_data['email']
            data.address_line_1 = orderform.cleaned_data['address_line_1']
            data.address_line_2 = orderform.cleaned_data['address_line_2']
            data.postcode = orderform.cleaned_data['postcode']
            data.country = orderform.cleaned_data['country']
            data.city = orderform.cleaned_data['city']
            data.delivery_method = orderform.cleaned_data['delivery_method']
            data.payment_method = orderform.cleaned_data['payment_method']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')

            # Utilisez une adresse IP spécifique pour simuler la localisation
            if settings.DEBUG:
                # Utilisation de l'API ipify pour obtenir une adresse IP publique
                response = requests.get('https://api.ipify.org?format=json')
                if response.status_code == 200:
                    ip_data = response.json()
                    user_ip = ip_data.get('ip')
                else:
                    # Fallback à une adresse IP locale si l'appel à l'API échoue
                    user_ip = '127.0.0.1'
            else:
                user_ip = request.META.get('REMOTE_ADDR')

            g = GeoIP2()
            try:
                user_country = g.country_code(user_ip)
                print(user_country)
                if user_country == 'FR':
                    orderform.fields['delivery_method'].initial = 'Colissimo'
                else:
                    orderform.fields['delivery_method'].initial = 'DHL'
            except Exception as e:
                print("Error determining user location:", e)

            # Déterminer le service de livraison en fonction de la localisation de l'utilisateur
            # user_ip = request.META.get('REMOTE_ADDR')
            # g = GeoIP2()
            # try:
            #     user_country = g.country_code(user_ip)
            #     print(user_country)
            #     if user_country == 'FR':
            #         orderform.fields['delivery_method'].initial = 'Colissimo'
            #     else:
            #         orderform.fields['delivery_method'].initial = 'DHL'
            # except Exception as e:
            #     print("Error determining user location:", e)

            data.save()

            # if orderform.cleaned_data['payment_method'] == "Card":
            #     return redirect('paypal_payment')
            # elif orderform.cleaned_data['payment_method'] == "Paypal":
            #     return redirect('stripe_payment')

            yr = int(datetime.date.today().strftime('%y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y-%m-%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total
            }

            return render(request, 'orders/payments.html', context)

    else:
        orderform = OrderForm()

    context = {
        'orderform': orderform,
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'orders/place-order.html', context)


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        subtotal = 0
        # tax = 0
        # grand_total = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
            # tax += (2*subtotal)/100
            # grand_total += subtotal + tax
        payment = Payment.objects.get(payment_id=transID)
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
            # 'tax': tax,
            # 'grand_total': grand_total,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('order_complete')

# def stripe_payment(request):
#     return render(request, 'orders/payments.html')

# def paypal_payment(request):
#     return render(request, 'orders/payments.html')

# orders views
