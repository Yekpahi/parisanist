from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
#paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
import orders
from orders.forms import OrderForm
from django.contrib import messages

from store.models import Product, Variation


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
# Add to cart
# Add to cart


def add_to_cart(request):
    # del request.session['cartdata']
    cart_p = {}
    cart_p[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'color':request.GET['color'],
        # 'size':request.GET['size'],
        'image': request.GET['image'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = int(
                cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})

# Cart List Page


def cart_list(request):
    tax = 0
    total_amt = 0
    grand_total = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty'])*float(item['price'])
        tax = (20*total_amt)/100
        grand_total = round((total_amt + tax), 2)
        return render(request, 'cart/cart.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt, 'tax': tax, 'grand_total': grand_total, })
    else:
        return render(request, 'cart/cart.html', {'cart_data': '', 'totalitems': 0, 'total_amt': total_amt, 'tax': tax, 'grand_total': grand_total, })

# Delete Cart Item


def delete_cart_item(request):
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata'] = cart_data
    tax = 0
    total_amt = 0
    grand_total = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty'])*float(item['price'])
    tax = (20*total_amt)/100
    grand_total = round((total_amt + tax), 2)
    t = render_to_string('cart/ajax/cart_list.html', {'cart_data': request.session['cartdata'], 'totalitems': len(
        request.session['cartdata']), 'total_amt': total_amt, 'total_amt':total_amt, 'tax':tax, 'grand_total':grand_total,})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})

# Delete Cart Item


# Delete Cart Item
def update_cart_item(request):
    p_id=str(request.GET['id'])
    p_qty=request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=p_qty
            request.session['cartdata']=cart_data
    tax=0
    total_amt=0
    grand_total=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
    tax = (20*total_amt)/100
    grand_total = round((total_amt + tax), 2)
    t=render_to_string('cart/ajax/cart_list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt, 'tax':tax, 'grand_total':grand_total,})
    return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})


# def cart(request, total=0, quantity=0, cart_items=None):
#     try:
#         tax = 0
#         grand_total = 0
#         if request.user.is_authenticated:
#             cart_items = CartItem.objects.filter(
#                 user=request.user, is_active=True)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.product_price*cart_item.quantity)
#             quantity += cart_item.quantity
#         tax = (20*total)/100
#         grand_total = round((total + tax), 2)

#     except ObjectDoesNotExist:
#         pass
#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#         'tax': tax,
#         'grand_total': grand_total
#     }
#     return render(request, 'cart/cart.html', context)


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

# Remove a Item


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(
            product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.product_price*cart_item.quantity)
            quantity += cart_item.quantity
        tax = (20*total)/100
        grand_total = round((total + tax), 2)

    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url='login')
def checkout(request):
    
    order_id='123'
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '123',
        'item_name': 'Item Name',
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    tax=0
    total_amt=0
    grand_total=0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*float(item['price'])
        tax = (20*total_amt)/100
        grand_total = round((total_amt + tax), 2)
        
        
        #payment methode
        # if request.method == 'POST':
        #     form = OrderForm(request.POST)
        #     if form.is_valid():
        #         order = form.save(commit=False)
        #         order.user = request.user
        #         order.save()
        #         if order.payment_method == 'Card':
        #             pass
        #             messages.success(request, 'Payment processed successfully via Credit Card.')
        #         elif order.payment_method == 'Paypal':
        #             order_id='123'
        #             host = request.get_host()
        #             paypal_dict = {
        #                 'business': settings.PAYPAL_RECEIVER_EMAIL,
        #                 'amount': '123',
        #                 'item_name': 'Item Name',
        #                 'currency_code': 'EU',
        #                 'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
        #                 'return_url': 'http://{}{}'.format(host,reverse('payment_done')),
        #                 'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
        #                 }
        #             form2 = PayPalPaymentsForm(initial=paypal_dict)
                    
        #             messages.success(request, 'Payment processed successfully via PayPal.')
        #         order.is_paid = True
        #         order.save()
        #         return redirect('order_detail', order_id=order.pk)
        # else:
        #     form = OrderForm()
            
        return render(request, 'checkout/checkout.html',
                  {'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),
                   'total_amt':total_amt, 'tax':tax, 'grand_total':grand_total, 'form':form})

            
@csrf_exempt
def payment_done(request):
	returnData=request.POST
	return render(request, 'payment_success.html',{'data':returnData})


@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment_fail.html')   

# def checkout(request, total=0, quantity=0, cart_items=None):
#     try:
#         tax = 0
#         grand_total = 0
#         if request.user.is_authenticated:
#             cart_items = CartItem.objects.filter(
#                 user=request.user, is_active=True)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         # cart = Cart.objects.get(cart_id=_cart_id(request))
#         # cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.product_price*cart_item.quantity)
#             quantity += cart_item.quantity
#         tax = (20*total)/100
#         grand_total = round((total + tax), 2)

#     except ObjectDoesNotExist:
#         pass
#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#         'tax': tax,
#         'grand_total': grand_total
#     }

#     return render(request, 'checkout/checkout.html', context)
