from django.db import models
# from django.urls import reverse
# from mptt.models import MPTTModel, TreeForeignKey

# class Category(MPTTModel):
#     category_name = models.CharField(max_length=100)
#     category_slug = models.SlugField(max_length= 100, unique=True)
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
#     category_description = models.TextField(max_length=200, blank = True)
    
#     class MPTTMeta:
#        order_insertion_by = ['category_name']

#     class Meta:
#         ordering = ('category_name',)
#         verbose_name = 'Category'
#         verbose_name_plural = 'Categories'

#     # def get_absolute_url(self):
#     #     return reverse('shop:product_list_by_category', args=[self.slug])

#     def __str__(self):
#         return self.category_name

    # def get_category_url(self):
    #     return reverse('boutique:category', kwargs={'gender': self.get_gender_display(), 'category_pk': self.pk})



class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_slug = models.SlugField(max_length= 100, unique=True)
    category_description = models.TextField(max_length=200, blank = True)
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    subcategory_name = models.TextField(max_length=100)
    category = models.ManyToManyField(Category)
    subcategory_slug = models.SlugField(max_length= 100, unique=True)
    subcategory_description = models.TextField(max_length=200, blank = True)
    
    class Meta:
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'
        
    def __str__(self):
         return self.subcategory_name + ' ' + str(self.category)
    