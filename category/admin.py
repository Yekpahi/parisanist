from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from category.models import Category, SubCategory

# class CategoryAdmin(DraggableMPTTAdmin) :
#     mptt_indent_field = "category_name"
#     mptt_indent_field = "name"
#     list_display = ('category_name', 'category_slug')
#     list_display_links = ('category_slug',)
#     prepopulated_fields = { "category_slug": ("category_name",),}

class CategoryAdmin(admin.ModelAdmin) :
    prepopulated_fields = { "subcategory_slug": ("subcategory_name",),}
    list_display = ['subcategory_name', 'subcategory_slug', 'categories']
    
class SubCategoryAdmin(admin.ModelAdmin) :
    prepopulated_fields = { "subcategory_slug": ("subcategory_name",),}
    list_display = ['subcategory_name', 'subcategory_slug', 'categories']
    
    def categories(self, obj):
        return "  - ".join([c.category_name for c in obj.category.all()])
  
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category)
# admin.site.register(SubCategory, SubCategoryAdmin)