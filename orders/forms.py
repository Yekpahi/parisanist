from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2',
                  'country', 'city', 'order_note', 'payment_method', 'delivery_method']
        widgets = {
            'delivery_method': forms.RadioSelect(),
            'payment_method': forms.RadioSelect(),
        }
        
# class PaymentMethodForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['payment-method']

# class DeriveryMethodForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['derivery-method']