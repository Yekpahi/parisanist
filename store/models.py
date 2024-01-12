from django.db import models
#from colorfield.fields import ColorField
from django.template.defaultfilters import slugify
from django.urls import reverse
from category.models import Category
from mptt.models import TreeForeignKey
# import PIL for image resizing
# from PIL import Image
# Create your models here.

#title, id, slug, image(s), price, category, subcategory, description, date, updated
# class Color(models.Model):
#     name = models.CharField(max_length=50)
#     def __str__(self) :
#         return self.name
# class Size(models.Model):
#     size = models.CharField(max_length=120,null=True,blank=True)

#     def __str__(self):
#         return self.size

class Product(models.Model): 
    product_name = models.CharField(max_length=500)
    product_slug = models.SlugField(null=True, blank=True)
    product_price = models.FloatField()
    product_stock =models.IntegerField(default = True)
    category = TreeForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    product_discountprice = models.FloatField(blank=True, null=True)
    product_description = models.TextField(null= True, blank=True)
    product_cleaning = models.TextField(null= True, blank=True)
    product_cover_image = models.ImageField(upload_to='static/cover/')
    is_active = models.BooleanField(default=False)
    is_active_active_on_home_carousel = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)    
    updated = models.DateTimeField(auto_now_add=True)
    
    def get_url(self) :
        return reverse('product_detail', args=[self.category.slug, self.product_slug])
    
    def price_without_tax(self):
        return str(self.product_price - self.product_price*20/100)
    
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

    # def __str__(self):
    #     return self.product_slug + " --- " + self.product_subcategory.category.category_name
          
class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos')
    photo_name = models.ImageField(upload_to ='stactic/photos/')
    photo_slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return str(self.photo_name) ### on met str(...) pour convertir en string
    @property
    def photoURL(self):
        try:
            url = self.photo_name.url
        except:
            url = ''
        print('URL :', url)
        return
	
	


# class ProductVariant(models.Model):
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     size = models.ForeignKey(Size, on_delete=models.CASCADE)
#     color = models.ForeignKey(Color,on_delete=models.CASCADE)
#     amount_in_stock = models.IntegerField()

#     def __str__(self) :
#         return self.product.title + "-" + self.color.name + "-" + self.size.size
    
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['product', 'color', 'size'],
#                 name='unique_prod_color_size_combo'
#             )
#         ]
    
