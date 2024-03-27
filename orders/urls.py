from django.urls import path
from orders import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments', views.payments, name = 'payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    # path('stripe-payment/', views.stripe_payment, name='stripe_payment'),
    # path('paypal-payment/', views.paypal_payment, name='paypal_payment'),
]