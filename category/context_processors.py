
from category.models import Category


def catmenu_links(request, category_slug=None):
    return {
        'catlinks': Category.objects.all()
    }