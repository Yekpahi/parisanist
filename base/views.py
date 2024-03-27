from django.shortcuts import redirect, render
from store.models import Product
from .forms import LaunchCountdownForm


def homepage(request):
    if request.method == 'POST':
        form = LaunchCountdownForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirection ou autre logique après avoir enregistré la date de lancement
    else:
        form = LaunchCountdownForm()
    products = Product.objects.all()[0:5]
    context = {
        'products': products,
        'form' : form
        
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


