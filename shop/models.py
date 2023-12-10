from django.db import models
#from colorfield.fields import ColorField
from django.template.defaultfilters import slugify
# import PIL for image resizing
from PIL import Image
# Create your models here.

#title, id, slug, image(s), price, category, subcategory, description, date, updated
class Color(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) :
        return self.name
class Size(models.Model):
    size = models.CharField(max_length=120,null=True,blank=True)

    def __str__(self):
        return self.size

###class Color(models.Model):
class Main_Category(models.Model) :
    name = models.CharField(max_length = 150)

    def __str__(self) :
        return self.name
class Category(models.Model):
    main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE)    
    name= models.CharField(max_length=150)
 
    def __str__(self):
        return self.name + "--" + self.main_category.name

class SubCategory(models.Model):
    name = models.CharField(max_length=150)
    categories = models.ManyToManyField(Category) 
    def __str__(self):
        return self.name

class Product(models.Model): 
    title = models.CharField(max_length=500)
    slug = models.SlugField(null=True, blank=True)
    price = models.FloatField()
    stock =models.IntegerField(default = True)
    category= models.ManyToManyField(SubCategory)
    discountprice = models.FloatField(blank=True, null=True)
    description = models.TextField(null= True, blank=True)
    product_cover_image = models.ImageField(upload_to='static/cover/')
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)    
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug
    
    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        img = Image.open(self.product_cover_image.path)
        if img.height > 1920 or img.width > 700:
           img.thumbnail((1920,700))
        img.save(self.product_cover_image.path,quality=70,optimize=True) 

           
class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to ='stactic/photos/')

    # resizing the image, you can change parameters like size and quality.
    def save(self, *args, **kwargs):
       super(Photo, self).save(*args, **kwargs)
       img = Image.open(self.photo.path)
       if img.height > 1125 or img.width > 1125:
           img.thumbnail((1125,1125))
       img.save(self.photo.path,quality=70,optimize=True)   
    def __str__(self):
        return str(self.photo) ### on met str(...) pour convertir en string
class ProductVariant(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    amount_in_stock = models.IntegerField()

    def __str__(self) :
        return self.product.title + "-" + self.color.name + "-" + self.size.size
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'color', 'size'],
                name='unique_prod_color_size_combo'
            )
        ]
    