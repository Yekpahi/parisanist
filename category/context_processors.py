
from category.models import Category, SubCategory


def menu_links(request):
    return {
        'catlinks': Category.objects.order_by("id").all(),
    }