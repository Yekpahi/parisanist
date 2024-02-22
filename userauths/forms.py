from django import forms
# from django.contrib.auth import get_user_model
from django.forms import ModelForm
from userauths.models import Account


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "register-all-input", "name": "first_name"}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "register-all-input", "name": "last_name"}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "register-all-input", "name": "username"}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={"class": "register-all-input", "name": "email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "register-all-input", "id":"myPass", "name":"password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "register-all-input", "id":"cmyPass", "name":"confirm_password"}))

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "username", "phone_number", "email", "password"]
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
    

        if password != confirm_password:
           raise forms.ValidationError(
             "Password does not match"
          )
    
    




# class UserRegisterForm(UserCreationForm):

#     firstname = forms.CharField(required=True, widget=forms.TextInput(
#         attrs={"placeholder": "First name"}))
#     username = forms.CharField(required=True, widget=forms.TextInput(
#         attrs={"placeholder": "Username"}))
#     lastname = forms.CharField(required=True, widget=forms.TextInput(
#         attrs={"placeholder": "Last name"}))
#     email = forms.EmailField(required=True, widget=forms.TextInput(
#         attrs={"placeholder": "Email"}))
#     password1 = forms.CharField(required=True, widget=forms.PasswordInput(
#         attrs={"placeholder": "Password"}))
#     password2 = forms.CharField(required=True, widget=forms.PasswordInput(
#         attrs={"placeholder": "Confirm password"}))

#     class Meta:
#         model = User
#         # User = get_user_model()
#         model = get_user_model()
#         fields = ('username', 'firstname', 'lastname', 'email', 'password1', 'password2', )
