from django.conf import settings
from django.db import models
from django.urls import reverse
import slugify
from category.models import Category
from mptt.models import TreeForeignKey

from userauths.models import Account


class Product(models.Model):
    product_name = models.CharField(max_length=500)
    product_slug = models.SlugField(null=False, blank=False)
    product_price = models.FloatField()
    itemNumber = models.PositiveIntegerField(unique=True, null=True, blank=True)
    product_stock = models.IntegerField(default=1)
    category = TreeForeignKey(Category, on_delete=models.CASCADE)
    product_discountprice = models.FloatField(blank=True, null=True)
    product_description = models.TextField(null=True, blank=True)
    product_cleaning = models.TextField(null=True, blank=True)
    product_home_carousel_image = models.ImageField(upload_to='static/cover/')
    is_active = models.BooleanField(default=False)
    is_active_on_home_carousel = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
                    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.id])

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
    
    def number(self):
        count = Variation.objects.count()
        if count == 0:
            return 1
        else:
            last_object = Variation.objects.order_by('-id')[0]
            return last_object.id + 1
    def save(self, *args, **kwargs):
        if not self.itemNumber:
            self.itemNumber=self.number()
        if not self.product_name:
            self.product_name = self.product.product_name + '-' + self.color.name
        if not self.product_slug:
            self.product_slug= slugify(self.product_name)
                
        context = super().save(*args, **kwargs)
        return context


class Color(models.Model):
    name=models.CharField(max_length=100, unique=True)
    colorCode=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Size(models.Model):
    size=models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return str(self.size)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_number = models.PositiveBigIntegerField(unique=True, null=True, blank=True)
    color=models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.product.product_name

class Discount(models.Model):
    name = models.CharField(max_length=250)
    discount = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name

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


