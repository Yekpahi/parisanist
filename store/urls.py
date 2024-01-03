from django.urls import path
from store import views


urlpatterns = [
    path('', views.store_page, name='store'),
    # path(r'^(?P<category_slug>[\w-]+)$', views.category),  
    path('<category_slug>/<subcategory_slug>', views.store_page, name='products_by_subcategory'), 
    #path('<str:category_slug>/', views.store_page, name='products_by_subcategory')
    #path('<slug:category_slug>/', views.store_page, name="products_by_category"),
]
