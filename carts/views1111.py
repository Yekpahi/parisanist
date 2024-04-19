from django.shortcuts import get_object_or_404, render, redirect
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from store.models import Color, Product, Size, Variation
# paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
import orders
from orders.forms import OrderForm
from django.contrib import messages
from django.db.models import Sum


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)  # to get the product
    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == "POST":
            size_id = request.POST.get('size')
            color_id = request.POST.get('color')

            # Retrieve the size and color objects from the database
            size = get_object_or_404(Size, id=size_id)
            color = get_object_or_404(Color, id=color_id)

            # Get the variation object for the selected size and color
            variation = Variation.objects.get(
                product=product, color=color, size=size)
            product_variation.append(variation)

            # Comptez le nombre total de commandes pour cette variation
            total_ordered = CartItem.objects.filter(variations=variation).aggregate(
                Sum('quantity'))['quantity__sum'] or 0
            if total_ordered >= variation.variation_number:
                messages.error(request, "Ce produit n'est pas disponible dans la variation sélectionnée.")
                print(messages)
                # Assurez-vous que cette URL est correcte
                return redirect('product_detail', category_slug=product.category.slug, product_slug=product.product_slug)

            # Create or update the cart item
            cart_item, created = CartItem.objects.get_or_create(
                user=current_user, product=product, defaults={'quantity': 1})

            # Instead of direct assignment, use the set() method for ManyToManyField
            cart_item.variations.set(product_variation)

            if not created:
                # If the cart item already exists, increment the quantity
                cart_item.quantity += 1
                cart_item.save()

            return redirect('cart')  # Redirect to the cart page
        is_cart_item_exists = CartItem.objects.filter(
            product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart_item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # create new cart_item
                item = CartItem.objects.create(
                    product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

    # if the user is not authenticated
    else:
        product_variation = []
        try:
            # get the cart_id present in the session #this will match the cart_id with session_id
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
        if request.method == 'POST':
            size_id = request.POST.get('size')
            color_id = request.POST.get('color')

            # Retrieve the size and color objects from the database
            size = get_object_or_404(Size, id=size_id)
            color = get_object_or_404(Color, id=color_id)

            # Get the variation object for the selected size and color
            variation = Variation.objects.get(product=product, color=color, size=size)
            product_variation.append(variation)
            
                 # Comptez le nombre total de commandes pour cette variation
            total_ordered = CartItem.objects.filter(variations=variation).aggregate(
                Sum('quantity'))['quantity__sum'] or 0
            if total_ordered >= variation.variation_number:
                messages.error(request, "Ce produit n'est pas disponible dans la variation sélectionnée.")
                print(messages)
                # Assurez-vous que cette URL est correcte
                return redirect('product_detail', category_slug=product.category.slug, product_slug=product.product_slug)

            # Create or update the cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, defaults={'quantity': 1})

            # Instead of direct assignment, use the set() method for ManyToManyField
            cart_item.variations.set(product_variation)

            if not created:
                # If the cart item already exists, increment the quantity
                cart_item.quantity += 1
                cart_item.save()

            return redirect('cart')  # Redirect to the cart page
            # color = request.POST['color'] #this color is coming from product_detail.html ->select option color
            # size = request.POST['size'] #this size is coming from product_detail.html ->select option size
            # print(key, value)

        is_cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing variations -> databse and current variation -> product_list  and item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart_item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # create new cart_item
                item = CartItem.objects.create(
                    product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

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
        'grand_total': grand_total,
        'messages': messages.get_messages(request)
    }
    return render(request, 'cart/cart.html', context)

def increment_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)  # to get the product
    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == "POST":
            size_id = request.POST.get('size')
            color_id = request.POST.get('color')

            # Retrieve the size and color objects from the database
            size = get_object_or_404(Size, id=size_id)
            color = get_object_or_404(Color, id=color_id)

            # Get the variation object for the selected size and color
            variation = Variation.objects.get(
                product=product, color=color, size=size)
            product_variation.append(variation)

            # Comptez le nombre total de commandes pour cette variation
            total_ordered = CartItem.objects.filter(variations=variation).aggregate(
                Sum('quantity'))['quantity__sum'] or 0
            if total_ordered >= variation.variation_number:
                messages.error(request, "Cette quantité n'est pas disponible pour se produit")
                print(messages)
                # Assurez-vous que cette URL est correcte
                return redirect('cart')

            # Create or update the cart item
            cart_item, created = CartItem.objects.get_or_create(
                user=current_user, product=product, defaults={'quantity': 1})

            # Instead of direct assignment, use the set() method for ManyToManyField
            cart_item.variations.set(product_variation)

            if not created:
                # If the cart item already exists, increment the quantity
                cart_item.quantity += 1
                cart_item.save()

            return redirect('cart')  # Redirect to the cart page
        is_cart_item_exists = CartItem.objects.filter(
            product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart_item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # create new cart_item
                item = CartItem.objects.create(
                    product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

    # if the user is not authenticated
    else:
        product_variation = []
        try:
            # get the cart_id present in the session #this will match the cart_id with session_id
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
        if request.method == 'POST':
            size_id = request.POST.get('size')
            color_id = request.POST.get('color')

            # Retrieve the size and color objects from the database
            size = get_object_or_404(Size, id=size_id)
            color = get_object_or_404(Color, id=color_id)

            # Get the variation object for the selected size and color
            variation = Variation.objects.get(product=product, color=color, size=size)
            product_variation.append(variation)
            
            # Comptez le nombre total de commandes pour cette variation
            total_ordered = CartItem.objects.filter(variations=variation).aggregate(
                Sum('quantity'))['quantity__sum'] or 0
            if total_ordered >= variation.variation_number:
                messages.error(request, "Cette quantité n'est pas disponible pour se produit")
                print(messages)
                # Assurez-vous que cette URL est correcte
                return redirect('cart')

            # Create or update the cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, defaults={'quantity': 1})

            # Instead of direct assignment, use the set() method for ManyToManyField
            cart_item.variations.set(product_variation)

            if not created:
                # If the cart item already exists, increment the quantity
                cart_item.quantity += 1
                cart_item.save()

            return redirect('cart')  # Redirect to the cart page
            # color = request.POST['color'] #this color is coming from product_detail.html ->select option color
            # size = request.POST['size'] #this size is coming from product_detail.html ->select option size
            # print(key, value)

        is_cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing variations -> databse and current variation -> product_list  and item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart_item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # create new cart_item
                item = CartItem.objects.create(
                    product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        # cart = Cart.objects.get(cart_id=_cart_id(request))
        # cart_items = CartItem.objects.filter(cart=cart, is_active=True)
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

    return render(request, 'checkout/checkout.html', context)



@csrf_exempt
def payment_done(request):
    returnData = request.POST
    return render(request, 'payment_success.html', {'data': returnData})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_fail.html')