from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2',
                  'country', 'state', 'city', 'order_note']
        
# class PaymentMethodForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['payment-method']

# class DeriveryMethodForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['derivery-method']