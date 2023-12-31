from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self,first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError("User must have an email username")
 
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name = first_name,
            last_name =last_name,
            )
        user.set_password(password)
        user.save()
        return user
 
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            username=username, 
            email=email, 
            password=password,
            first_name= first_name,
            last_name=last_name,
            )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(blank=False, null=False, max_length=200)
    last_name = models.CharField(blank=False, null=False, max_length=200)
    phone_number = models.CharField(max_length=50)
    #Required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    
    objects = AccountManager()
    def __str__(self):
        return f"{self.first_name } {self.last_name}"
    def has_perm(self, perm, obj = None) :
        return self.is_admin
    def has_module_perms(self, add_label):
        return True
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     firstname = models.CharField(max_length=100, blank=True)
#     lastname = models.CharField(max_length=100, blank=True)
#     email = models.EmailField(max_length=150)
#     signup_confirmation = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.username

# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()