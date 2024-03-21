from django.shortcuts import render
from store.models import Product
from django.contrib.gis.geoip2 import GeoIP2

# Create your views here.


def homepage(request):
    products = Product.objects.all()[0:5]
    context = {
        'products': products,
        
        }
    return render(request, "base/home.html", context)

def about(request):
    return render(request, "base/about.html")

def privacy(request):
    return render(request, "base/privacy.html")

def terms(request):
    return render(request, "base/terms.html")

def legalNotice(request):
    return render(request, "base/legalNotice.html")

def refund(request):
    return render(request, "base/refund.html")
def shipping(request):
    return render(request, "base/shipping.html")


