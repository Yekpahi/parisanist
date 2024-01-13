from django.shortcuts import get_object_or_404, render
from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from store.models import Photo, Product

# Create your views here.

# def store_page(request, category_slug = None, ):
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(is_active=True).order_by('-created')

#     if category_slug != None :
#         category = get_object_or_404(Category, subcategory_slug=category_slug)
#         sub_categories = category.get_descendants(include_self=True)
#         products = products.filter(product_category=sub_categories)
#         product_count = products.count()
#     else:
#         products = Product.objects.all().filter(is_active = True)
#         product_count = products.count()
#     context = {
#         'category': category,
#         'products': products,
#         'categories': categories,
#         'product_count' : product_count
#         }
#     return render(request, "store/store.html", context)


# def store_page(request, subcategory_slug=None, category_slug=None):
#     subcategories = None
#     products = None
#     if subcategory_slug != None :
#         subcategories = get_object_or_404(SubCategory, subcategory_slug=subcategory_slug)
#         products = Product.objects.filter(product_subcategory=subcategories,  is_active=True)
#         product_count = products.count()
#     else:
#         products = Product.objects.all().filter(is_active=True)
#         product_count = products.count()
#     context = {
#         'products': products,
#         'subcategories': subcategories,
#         'product_count': product_count
#     }
#     return render(request, "store/store.html", context)

# def store_cat(request, category_slug=None):
#     categories = None
#     products = None
#     if category_slug != None :
#         categories = get_object_or_404(Category, category_slug=category_slug)
#         products = Product.objects.filter(product_category=categories,  is_active=True)
#         product_count = products.count()
#     else:
#         products = Product.objects.all().filter(is_active=True)
#         product_count = products.count()
#     context = {
#         'products': products,
#         'categories': categories,
#         'product_count': product_count
#     }
#     return render(request, "store/store.html", context)

def product_list(request, category_slug=None, sub_categories=None, product_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True).order_by('-created')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        sub_categories = category.get_descendants(include_self=True)
        products = products.filter(category__in=sub_categories)
        product_count = products.count()
        
    else :
        products = Product.objects.filter(is_active=True).order_by('-created')
        product_count = products.count()

    return render(request,
                  'store/store.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'product_count' : product_count
                   })

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