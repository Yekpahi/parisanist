from django.shortcuts import get_object_or_404, render, redirect
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


from store.models import Product, Variation

def _cart_id(request):
    cart = request.session.session_key
    if not cart :
        cart = request.session.create()
    return cart

def add_cart(request, product_id) :
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
           key = item
           value = request.POST[key]
           
           try :
               variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value_iexact=value)
               product_variation.append(variation)
           except:
               pass     
    try :
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    
    try:
        cart_item= CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1 :
        cart_item.quantity -= 1
        cart_item.save()
    else :
        cart_item.delete()
   
    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart') 
    
def cartviews(request, total = 0, quantity = 0, cart_items = None):
    try :
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.product_price*cart_item.quantity)
            quantity += cart_item.quantity
        tax = (20*total)/100
        grand_total = round((total - tax), 2)
    
    except ObjectDoesNotExist:
        pass 
    context = {
        'total':total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total': grand_total
    }
    return render(request, 'cart/cart.html', context)
