from django.db import models
from django.urls import reverse
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length= 100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    description = models.TextField(max_length=200, blank = True)
    
    class MPTTMeta:
       order_insertion_by = ['name']

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.name

#     def get_category_url(self):
#         return reverse('boutique:category', kwargs={'gender': self.get_gender_display(), 'category_pk': self.pk})
# class Category(models.Model):
#     category_name = models.CharField(max_length=100)
#     category_slug = models.SlugField(max_length= 100, unique=True)
#     category_description = models.TextField(max_length=200, blank = True)
#     @staticmethod
#     def get_all_categories():
#         return Category.objects.all()
    
#     class Meta:
#         verbose_name = 'category'
#         verbose_name_plural = 'categories'
    
#     def __str__(self):
#         return self.category_name
    
#     def get_absolute_url(self):
#         return reverse('products_by_category', args=[self.category_slug])

# class SubCategory(models.Model):
#     subcategory_name = models.TextField(max_length=100)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     subcategory_slug = models.SlugField(max_length= 100, unique=True)
#     subcategory_description = models.TextField(max_length=200, blank = True)
    
#     class Meta:
#         verbose_name = 'subcategory'
#         verbose_name_plural = 'subcategories'
        
#     def __str__(self):
#          return self.subcategory_name + " - " + self.category.category_name   
    
#     def get_url(self):
#         return reverse('products_by_subcategory', args=[self.subcategory_slug])
    
       