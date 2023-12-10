from django.contrib import admin

# Register your models here.
from .models import Category, Photo, Product, ProductVariant, Size, SubCategory, Main_Category, Color
class PhotoAdmin(admin.StackedInline):
    model = Photo

class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoAdmin]
    list_display = ('title', 'price', 'discountprice', 'stock', 'is_active', 'updated')
    
    class Meta:
        model = Product

admin.site.register(Photo)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Main_Category)
admin.site.register(Category)
admin.site.register(SubCategory)