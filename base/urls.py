
from django.urls import path
from base import views


urlpatterns = [
    path('home/', views.homepage, name='home'),
    path('store/', views.storepage, name='store')
]
