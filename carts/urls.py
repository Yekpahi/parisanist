from django.urls import path
from carts import views
urlpatterns = [
    path('', views.cartviews, name='cart'),
    path('add-to-cart',views.add_to_cart,name='add_to_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name ="checkout")
]
