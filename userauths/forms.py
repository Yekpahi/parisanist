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
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "register-all-input", "id":"cmyPass", "name":"password2"}))

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "username", "phone_number", "email", "password"]

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = Account.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name'].lower()
        r = Account.objects.filter(first_name=first_name)
        if r.count():
            raise forms.ValidationError("First name already exists")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name'].lower()
        r = Account.objects.filter(last_name=last_name)
        if r.count():
            raise forms.ValidationError("Last name already exists")
        return last_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

