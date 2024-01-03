from django.shortcuts import render
from store.models import Product
# Create your views here.


def homepage(request):
    products = Product.objects.all()[0:4]
    context = {'products': products}
    return render(request, "base/home.html", context)

def about(request):
    return render(request, "base/about.html")
