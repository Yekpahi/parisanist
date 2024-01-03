from django.shortcuts import get_object_or_404, render
from category.models import Category, SubCategory

from store.models import Product

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


def store_page(request, category_slug=None, subcategory_slug=None):
    subcategories = None
    categories = None
    products = None

    if subcategory_slug != None and category_slug != None:
        subcategories = get_object_or_404(
            SubCategory, subcategory_slug=subcategory_slug)
        categories = get_object_or_404(Category, category_slug=category_slug)
        products = Product.objects.filter(
            product_subcategory=subcategories, product_category=categories, is_active=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_active=True)
        product_count = products.count()
    context = {
        'products': products,
        'subcategories': subcategories,
        'categories': categories,
        'product_count': product_count
    }
    return render(request, "store/store.html", context)
