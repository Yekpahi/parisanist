from django.contrib import admin
from category.models import Category, SubCategory


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"category_slug": ("category_name",), }
    list_display = ['category_name', 'category_slug']


class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"subcategory_slug": ("subcategory_name",), }
    list_display = ['subcategory_name', 'subcategory_slug', 'categories']

    def categories(self, obj):
        return "  - ".join([c.category_name for c in obj.category.all()])


admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category,  CategoryAdmin)
