from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from store.models import Photo, Product, Variation, Wishlist
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

def product_list(request, category_slug=None, product_slug=None):
    wishlisted_list =[]
    if request.user.is_authenticated:
        wishlisted_list = list(Wishlist.objects.filter(user_id=request.user).values_list('product_id',flat=True).order_by('product_id'))
    
    
    category = None
    categories = Category.objects.all()
    # for printint only the parents
    parents = Category.objects.filter(parent=None)
    # End for printint only the parents

    # filter by product variation
    # variations = Variation.objects.distinct().values('variation_value')
    variations = Variation.objects.distinct().values('variation_value', 'product_id')

    # sort by
    sort_by = request.GET.get("sort", "l2h")
    if sort_by == "l2h":
        products = Product.objects.filter(
            is_active=True).order_by('product_price')
    elif sort_by == "h2l":
        products = Product.objects.filter(
            is_active=True).order_by('-product_price')
    # end sort by
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        sub_categories = category.get_descendants(include_self=True)
        products = products.filter(category__in=sub_categories)
        # paginator = Paginator(products, 2)
        # page = request.GET.get('page')
        # paged_products = paginator.get_page(page)
        product_count = products.count()
    else:

        # sort by
        sort_by = request.GET.get("sort", "l2h")
        if sort_by == "l2h":
            products = Product.objects.filter(
                is_active=True).order_by('product_price')
        elif sort_by == "h2l":
            products = Product.objects.filter(
                is_active=True).order_by('-product_price')
        product_count = products.count()

    varID = request.GET.get('varID')
    if varID:
        product = Product.objects.filter(variation=varID)
    else:
        product = Product.objects.all()
    return render(request,
                  'store/store.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'product_count': product_count,
                   'parents': parents,
                   'variations': variations,
                   'product': product,
                   'wishlisted_list':wishlisted_list
                   })


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

@login_required
def wishlist(request):
    wishlist = Wishlist.objects.all()
    context = {
        "w":wishlist
    }
    return render(request, "store/wishlist.html", context)


@login_required
def add_to_wishlist(request):
    if request.accepts('text/html') and request.POST and 'attr_id' in request.POST:
        if request.user.is_authenticated:
            data = Wishlist.objects.filter(user_id = request.user.pk, product_id = int(request.POST['attr_id']))
            print(data)
            if data.exists():
                data.delete()
            else:
                Wishlist.objects.create(user_id = request.user.pk,product_id = int(request.POST['attr_id']))
    else:
        print("No Product is Found")

    return redirect("home")

# def add_to_wishlist(request):
#     if request.method == 'POST':
#         product = get_object_or_404(Product, pk=request.POST.get('id'))
#         Wishlist.objects.get_or_create(user=request.user, product=product)
#         return HttpResponseRedirect(reverse('wishlist'))


"""
def add_to_wishlist(request):

    product_id = request.GET['id']
    # product = get_object_or_404(Product, id=request.Product.get('product_id'))
    product = Product.objects.get(id = product_id)
    print("product Id is :" + product_id)
    
    context = {}
    wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
    if wishlist_count > 0 :
        context = {
            "bool": True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            user=request.user,
            product=product,
           
        )
        context = {
            "bool": True,
        }
        
    return JsonResponse(context)
"""
def remove_wishlist(request):
    pid = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user).count()
    wishlist_id = Wishlist.objects.get(id=pid)
    delete_product = wishlist_id.delete()
    context = {
        "bool": True,
        'wishlist':wishlist
    }
    
    t = render_to_string('store/async/wishlist_list.html', context)
    
    return JsonResponse({'data' :t, 'all_wishlist':wishlist})
     