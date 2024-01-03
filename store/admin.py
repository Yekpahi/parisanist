from django.contrib import admin

# Register your models here.
from .models import Photo, Product
class PhotoAdmin(admin.StackedInline):
    model = Photo
    list_display = ['product_name', 'product_slug']
    prepopulated_fields = {'photo_slug': ('photo_name',),}

class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoAdmin]
    list_display = ['product_name', 'product_price', 'product_discountprice', 'product_stock', 'is_active', 'updated',]
    prepopulated_fields = {'product_slug': ('product_name',),}
    
    # def subcategories(self, obj):
    #     return "  - ".join([sb.subcategory_name for sb in obj.product_subcategory.all()])
    
    class Meta:
        model = Product
admin.site.register(Product, ProductAdmin)
