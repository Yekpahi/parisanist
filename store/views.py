from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from store.models import Color, Photo, Product, Size, Variation, Wishlist
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string


def product_list(request, category_slug=None, product_slug=None):
    wishlisted_list = []
    if request.user.is_authenticated:
        wishlisted_list = list(Wishlist.objects.filter(user_id=request.user).values_list(
            'product_id', flat=True).order_by('product_id'))

    category = None
    products = None
    categories = Category.objects.all()
    # for printint only the parents
    parents = Category.objects.filter(parent=None)
    # End for printint only the parents

    # Start filter by product variation
    colors = Variation.objects.distinct().values(
        'color__name', 'color__id', 'color__colorCode')
    sizes = Variation.objects.distinct().values('size__size', 'size__id')
    # End filter by product variation
       
    # start Size color and filter
    SizeId = request.GET.get('sizeID')
    ColorId = request.GET.get('colorID')
    # End Size color and filter
    # Start sortby
    sort_by = request.GET.get("sort", "l2h")
    # End sortby
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        sub_categories = category.get_descendants(include_self=True)
        products = Product.objects.filter(category__in=sub_categories)
     # start Size color and filter
    elif SizeId:
        products = Product.objects.filter(variation__size__id__in=SizeId)
    elif ColorId:
        products = Product.objects.filter(variation__color__id__in=ColorId)
    # End Size color and filter
    # Start sortby
    elif sort_by == "l2h":
         products = Product.objects.filter(is_active=True).order_by('product_price')
    elif sort_by == "h2l":
         products = Product.objects.filter(is_active=True).order_by('-product_price')
    # end sort by
    # start Size color and filter
    else:
        products = Product.objects.all().filter(is_active=True)


    return render(request,
                  'store/store.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'parents': parents,
                    # 'productx': productx,
                   'sizes': sizes,
                   'colors': colors,
                   'wishlisted_list': wishlisted_list
                   })
    
# filter data
def filter_data(request):
    colors = request.GET.getlist('color[]')
    sizes = request.GET.getlist('size[]')
    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(colors) > 0:
        allProducts = allProducts.filter(
            variation__color__id__in=colors).distinct()
    if len(sizes) > 0:
        allProducts = allProducts.filter(
            variation__size__id__in=sizes).distinct()
    t = render_to_string('ajax/product-list.html', {'data': allProducts})
    return JsonResponse({'data': t})


# def filter_data(request):
#     colors = request.GET.getlist('color[]')
#     sizes = request.GET.getlist('size[]')
#     allProducts = Product.objects.all().order_by('-id').distinct()
#     if len(colors) > 0:
#         allProducts = allProducts.filter(
#             variation__color__id__in=colors).distinct()
#     if len(sizes) > 0:
#         allProducts = allProducts.filter(
#             variation__size__id__in=sizes).distinct()
#     t = render_to_string('store/store.html', {'data': allProducts})
#     print(colors)
#     return JsonResponse({'data': t})


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created').filter(
                Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count
    }
    return render(request,  'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, product_slug=product_slug)
        # details images
        images = Photo.objects.filter(product=single_product)
        # if item is already in the cart
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product)

    except Exception as e:
        raise
    context = {
        'single_product': single_product,
        'images': images,
        'in_cart': in_cart
    }
    return render(request, 'store/product-details/product_details.html', context)

# Wishlist


@login_required
def add_wishlist(request):
    pid = request.GET['product']
    product = Product.objects.get(pk=pid)
    data = {}
    checkw = Wishlist.objects.filter(
        product=product, user=request.user).count()
    if checkw > 0:
        data = {
            'bool': False
        }
    else:
        wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
        data = {
            'bool': True
        }
    return JsonResponse(data)


@login_required
# My Wishlist
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user).order_by('-id')
    context = {
        "wishlist": wishlist
    }
    return render(request, "user/dashboard/wishlist.html", context)


# def add_to_wishlist(request):
#     if request.accepts('text/html') and request.POST and 'attr_id' in request.POST:
#         if request.user.is_authenticated:
#             data = Wishlist.objects.filter(
#                 user_id=request.user.pk, product_id=int(request.POST['attr_id']))
#             print(data)
#             if data.exists():
#                 data.delete()
#             else:
#                 Wishlist.objects.create(
#                     user_id=request.user.pk, product_id=int(request.POST['attr_id']))
#     else:
#         print("No Product is Found")

#     return redirect("home")

# def add_to_wishlist(request):
#     if request.method == 'POST':
#         product = get_object_or_404(Product, pk=request.POST.get('id'))
#         Wishlist.objects.get_or_create(user=request.user, product=product)
#         return HttpResponseRedirect(reverse('wishlist'))


# def add_to_wishlist(request):

#     product_id = request.GET['id']
#     # product = get_object_or_404(Product, id=request.Product.get('product_id'))
#     product = Product.objects.get(id = product_id)
#     print("product Id is :" + product_id)

#     context = {}
#     wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
#     if wishlist_count > 0 :
#         context = {
#             "bool": True
#         }
#     else:
#         new_wishlist = Wishlist.objects.create(
#             user=request.user,
#             product=product,

#         )
#         context = {
#             "bool": True,
#         }

#     return JsonResponse(context)


def remove_wishlist(request):
    pid = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user).count()
    wishlist_id = Wishlist.objects.get(id=pid)
    delete_product = wishlist_id.delete()
    context = {
        "bool": True,
        'wishlist': wishlist
    }

    t = render_to_string('store/async/wishlist_list.html', context)

    return JsonResponse({'data': t, 'all_wishlist': wishlist})
