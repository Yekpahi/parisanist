from django import forms
# from django.contrib.auth import get_user_model
from django.forms import ModelForm
from userauths.models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Confirm Password"}))

    class Meta:
        model = Account
        fields = ["first_name", "last_name",
                  "phone_number", "email", "password"]
    
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
