from store.models import Variation


def get_filters(request):
    colors = Variation.objects.distinct().values('color__name', 'color__id', 'color__colorCode')
    
    sizes = Variation.objects.distinct().values('size__size', 'size__id')
    data = {
        'colors': colors,
        'sizes':sizes
    }
    return data