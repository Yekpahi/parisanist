from django.db import models
#from colorfield.fields import ColorField
from django.template.defaultfilters import slugify
from category.models import Category, SubCategory
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
    product_subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='services')
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    product_discountprice = models.FloatField(blank=True, null=True)
    product_description = models.TextField(null= True, blank=True)
    product_cover_image = models.ImageField(upload_to='static/cover/')
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)    
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_slug
     
# class Product(models.Model): 
#     product_name = models.CharField(max_length=500)
#     product_slug = models.SlugField(null=True, blank=True)
#     product_price = models.FloatField()
#     product_stock =models.IntegerField(default = True)
#     product_category = TreeForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
#     product_discountprice = models.FloatField(blank=True, null=True)
#     product_description = models.TextField(null= True, blank=True)
#     product_cover_image = models.ImageField(upload_to='static/cover/')
#     is_active = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)    
#     updated = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.product_slug
          
class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos')
    photo_name = models.ImageField(upload_to ='stactic/photos/')
    photo_slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return str(self.photo_name) ### on met str(...) pour convertir en string
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
    
