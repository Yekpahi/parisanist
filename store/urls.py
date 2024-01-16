from django.urls import path
from store import views


urlpatterns = [
    path('', views.product_list, name='store'),
    # path(r'^categories/$', views.product_list, name = "products_by_category"), 
    path('category<slug:category_slug>/', views.product_list, name='products_by_category'), 
    path('category/<slug:category_slug>/<slug:product_slug>', views.product_detail, name="product_detail"),
    path('search/', views.search, name = 'search'),
]