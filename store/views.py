from django.shortcuts import get_object_or_404, render
from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from store.models import Photo, Product
from django.db.models import Q
from django.core.paginator import EmptyPage, Paginator, Paginator


def product_list(request, category_slug=None, product_slug=None):
    category = None
    categories = Category.objects.all()
    # for printint only the parents
    parents = Category.objects.filter(parent=None)

    products = Product.objects.filter(is_active=True).order_by('-created')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        sub_categories = category.get_descendants(include_self=True)
        products = products.filter(category__in=sub_categories)
        paginator = Paginator(products, 2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        
    else :
        products = Product.objects.filter(is_active=True).order_by('-created')
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    return render(request,
                  'store/store.html',
                  {'category': category,
                   'categories': categories,
                   'products': paged_products,
                   'product_count' : product_count,
                   'parents' : parents
                   })
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created').filter(Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count
    }
    return render(request,  'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, product_slug=product_slug)
        # details images
        images = Photo.objects.filter(product=single_product)
        # if item is already in the cart
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product = single_product)

    except Exception as e:
        raise 
    context = {
    'single_product' : single_product,
    'images':images,
    'in_cart' : in_cart
    }
    return render(request, 'store/product_detail.html', context)



