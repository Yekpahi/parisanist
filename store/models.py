from django.conf import settings
from django.db import models
from django.urls import reverse
from category.models import Category
from mptt.models import TreeForeignKey

from userauths.models import Account


class Product(models.Model):
    product_name = models.CharField(max_length=500)
    product_slug = models.SlugField(null=False, blank=False)
    product_price = models.FloatField()
    product_stock = models.IntegerField(default=True)
    category = TreeForeignKey(Category, on_delete=models.CASCADE)
    product_discountprice = models.FloatField(blank=True, null=True)
    product_description = models.TextField(null=True, blank=True)
    product_cleaning = models.TextField(null=True, blank=True)
    # product_cover_image = models.ImageField(upload_to='static/cover/')
    product_home_carousel_image = models.ImageField(upload_to='static/cover/')
    is_active = models.BooleanField(default=False)
    is_active_active_on_home_carousel = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.product_slug])

    def price_with_tax(self):
        return str(self.product_price + self.product_price*20/100)

    def __str__(self):
        return self.product_slug

    @property
    def photoURL(self):
        try:
            url = self.product_cover_image.url
        except:
            url = ''
        print('URL :', url)
        return url

class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    product =models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "wishlists"
    def __str__(self):
        return self.product.product_name
   
class Photo(models.Model):
    title = models.CharField(max_length=500, blank=True, null = True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='photos')
    # photo_name = models.ImageField(upload_to='stactic/photos/', verbose_name=("image"))
    product_image = models.ImageField(upload_to='stactic/photos/', verbose_name=("image"))
    photo_slug = models.SlugField(null=True, blank=True)
    is_feature=models.BooleanField(default=False)
    def __str__(self):
        return str(self.product_image)  # on met str(...) pour convertir en string

    @property
    def photoURL(self):
        try:
            url = self.photo_name.url
        except:
            url = ''
        print('URL :', url)
        return

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_available=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_available=True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    created_date = models.DateField(auto_now=True)

    objects = VariationManager()
    def __str__(self):
        return self.variation_value
    
