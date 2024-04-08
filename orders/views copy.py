import json
from django.urls import reverse
import requests
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseServerError, JsonResponse
from django.shortcuts import render
import datetime
from django.shortcuts import render, redirect
import stripe
from carts.models import Cart, CartItem
from store.models import Product
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import send_mail
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY



def paypal_paymentx(request, payment_method=None, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    # Calculate total, tax, and grand total
    for cart_item in cart_items:
        total += (cart_item.product.product_price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (20 * total) / 100
    taxdhl = 50
    grand_total = round((total + tax), 2)
    grand_total_dhl = grand_total + taxdhl

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
 
         # Store the payment details in the Payment Model

        # Store payment details in DB
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        #  Get order having the order number
        order = Order.objects.get(user=request.user, order_number=order_number)
        # payment model
        payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            amount = order.total,
            status = status
        )

        # save the payment model now
        payment.save()


        # Update the ORDER MODEL
        order.payment = payment
        order.is_ordered = True
        order.save()

        # Create OrderProduct instances for each cart item
        for item in cart_items:
            orderproduct = OrderProduct.objects.create(
                order=order,
                payment=payment,
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                product_price=item.product.product_price,
                ordered=True
            )
            orderproduct.variations.set(item.variations.all())

            # Reduce product stock
            product = item.product
            product.product_stock -= item.quantity
            product.save()

        # Clear cart
        CartItem.objects.filter(user=request.user).delete()

        # Send order received email to customer
        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_received_email.html', {
            'user': request.user,
            'order': order,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        # Prepare data to pass to the template
        data = {
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'order': order
        }
        
        # Render the payments.html template with the data
        return JsonResponse(data)
    else:
        # Pass data to the template if the request is not AJAX or not POST
        context = {
            'cart_items': cart_items,
            'total': total,
            'tax': tax,
            'taxdhl': taxdhl,
            'grand_total': grand_total,
            'grand_total_dhl': grand_total_dhl
        }
        return render(request, 'orders/payments.html', context)

def paypal_paymentt(request, payment_method=None, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    grand_total_dhl = 0
    taxdhl = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.product_price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (20 * total) / 100
    taxdhl = 50
    grand_total = round((total + tax), 2)
    grand_total_dhl += grand_total + taxdhl
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        body = json.loads(request.body)
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

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

        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct.objects.create(
                order=order,
                payment=payment,
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                product_price=item.product.product_price,
                ordered=True
            )
            orderproduct.variations.set(item.variations.all())

            product = Product.objects.get(id=item.product_id)
            product.product_stock -= item.quantity
            product.save()

        CartItem.objects.filter(user=request.user).delete()

        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_received_email.html', {
            'user': request.user,
            'order': order,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        data = {
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'order':order
        }
        
        return render(request, 'orders/payments.html', data)
    else:
       pass 
    # Passer les informations au template si la requête n'est pas AJAX ou si la méthode n'est pas POST
    context = {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'taxdhl': taxdhl,
        'grand_total': grand_total,
        'grand_total_dhl': grand_total_dhl
    }
    return render(request, 'orders/payments.html', context)


def paypal_paymentc(request, payment_method=None):
    # Check if the request is AJAX or not

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        # Store the payment details in the Payment Model

        # Store payment details in DB
        # order_number = request.POST.get('order_number')
        # transaction_id = request.POST.get('transaction_id')
        # payment_method = request.POST.get('payment_method')
        # status = request.POST.get('status')

        # #  Get order having the order number
        # order = Order.objects.get(user=request.user, order_number=order_number)
        body = json.loads(request.body)
        order = Order.objects.get(
            user=request.user, is_ordered=False, order_number=body['orderID'])
        # payment model
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

        # Move the CART ITEMS to ORDERED FOOD MODEL
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
    return render(request, 'orders/payments.html')


def paypal_payment(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

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

#Stripe payment
def stripe_payment(request):
    cart = Cart(request)
    data = json.loads(request.body)
    total_price = 0

    items = []

    for item in cart:
        product = item['product']
        total_price += product.price * int(item['quantity'])

        items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': product.price,
            },
            'quantity': item['quantity']
        })
    
    stripe.api_key = settings.STRIPE_API_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('stripe_success')),
        cancel_url=request.build_absolute_uri(reverse('stripe_cancel')),
    )
    payment_intent = session.payment_intent

    order = Order.objects.create(
        user=request.user, 
        first_name=data['first_name'], 
        last_name=data['last_name'], 
        email=data['email'], 
        phone=data['phone'], 
        address_line_1=data['address_line_1'], 
        address_line_2=data['address_line_2'], 
        zip_code=data['zip_code'], 
        country=data['country'],
        city=data['city'],
        payment_intent=payment_intent,
        is_ordered=True,
        amount_paid=order.order_total
    )

    for item in cart:
        product = item['product']
        quantity = int(item['quantity'])
        price = product.product_price * quantity

        item = OrderProduct.objects.create(order=order, product=product, price=price, quantity=quantity)

    cart.clear()

    return JsonResponse({'session': session, 'order': payment_intent})



def stripe_paymentss(request):
    body = json.loads(request.body)

    # Create or retrieve order
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Create a new Stripe Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Product Name',
                    },
                    'unit_amount': int(order.order_total * 100),  # Amount in cents
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('stripe_success')),
        cancel_url=request.build_absolute_uri(reverse('stripe_cancel')),
    )

    # Store transaction details inside Payment model
    payment = Payment(
        user=request.user,
        payment_id=session.payment_intent,
        payment_method='Stripe',  # Assuming payment method is Stripe
        amount_paid=order.order_total,
        status='Pending',  # Assuming initial status is pending
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

    # Send order received email to customer
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

def stripe_paymentc(request):
    # Create a new Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Product Name',
                    },
                    'unit_amount': 1000,  # Amount in cents
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('stripe_success')),
        cancel_url=request.build_absolute_uri(reverse('stripe_cancel')),
    )

    return redirect(session.url)

def stripe_success(request):
    return render(request, 'orders/success.html')

def stripe_cancel(request):
    return render(request, 'orders/cancel.html')

#Orders
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    grand_total_dhl = 0
    taxdhl = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.product_price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (20 * total) / 100
    taxdhl = 50
    grand_total = round((total + tax), 2)
    grand_total_dhl += grand_total + taxdhl

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
            payment_method = orderform.cleaned_data.get('payment_method')
            data.delivery_method = orderform.cleaned_data['delivery_method']
            # data.payment_method = orderform.cleaned_data['payment_method']
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

            # if payment_method == "Card":
            #     return redirect('stripe_payment')

            # elif  payment_method == "Paypal":
            #     return redirect('paypal_payment')
            # else :
            #     pass

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
                'taxdhl': taxdhl,
                'grand_total': grand_total,
                'grand_total_dhl': grand_total_dhl
            }

            return render(request, 'orders/payments.html', context)
    else:
        orderform = OrderForm()

    context = {
        'orderform': orderform,
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'taxdhl': taxdhl,
        'grand_total': grand_total,
        'grand_total_dhl': grand_total_dhl
    }
    return render(request, 'orders/place_order.html', context)


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        subtotal = 0
        tax = 0
        grand_total = 0
        grand_total_dhl=0
        
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
            tax += (2*subtotal)/100
            taxdhl = 50
            grand_total += subtotal + tax
            grand_total_dhl += grand_total + taxdhl

        payment = Payment.objects.get(payment_id=transID)
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
            'tax': tax,
            'taxdhl': taxdhl,
            'grand_total': grand_total,
            'grand_total_dhl': grand_total_dhl
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('order_complete')

