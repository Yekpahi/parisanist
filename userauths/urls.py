
from django.urls import path
from userauths import views



urlpatterns = [
      # Add this path
    path('register/', views.register, name= "register"),  
    path('login/', views.login, name= "login"),
    path('logout/', views.logout, name ="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name= "resetpassword_validate"),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path("wishlist/add_to_wishlist/<int:id>", views.add_to_wishlist, name="user_wishlist"),
]
