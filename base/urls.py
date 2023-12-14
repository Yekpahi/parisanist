
from django.urls import path
from base import views


urlpatterns = [
    path('', views.homepage, name='home'),
    path('about/', views.about, name= "about"),
    path('store/', views.storepage, name='store')
]
