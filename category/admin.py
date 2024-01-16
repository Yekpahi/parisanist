from django.contrib import admin
from category.models import Category
from mptt.admin import DraggableMPTTAdmin


admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'parent',
        'name',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'name',
    ),
    prepopulated_fields = {'slug': ('name',),}
)



# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"category_slug": ("category_name",), }
#     list_display = ['category_name', 'category_slug']


# class SubCategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"subcategory_slug": ("subcategory_name",), }
#     list_display = ['subcategory_name', 'subcategory_slug']

# def categories(self, obj):
#     return "  - ".join([c.category_name for c in obj.category.all()])


# admin.site.register(SubCategory, SubCategoryAdmin)
# admin.site.register(Category,  CategoryAdmin)
