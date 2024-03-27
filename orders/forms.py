from django import forms
from .models import Order

COUNTRY_CHOICES = [
    ('US', 'United States'),
    ('FR', 'France'),
    ('CIV', "Côte d'Ivoire"),
    ('BN', 'Benin'),
    ('It', 'Italie'),
    ('ALL', 'Allemagne'),
    ('CA', "Canada"),
    ('Be', 'Belgique'),
    # Add more countries as needed
]

ZIP_CHOICES = [
    ('+1', 'United States +1'),
    ('+33', 'France +33'),
    ('+225', "Côte d'Ivoire +225"),
    ('+226', 'Benin +226'),
    ('+42', 'Italie +42'),
    ('+4', 'Allemagne +4'),
    ('+1', "Canada +1"),
    ('+34', 'Belgique +34'),
    # Add more countries as needed

]
 
DELIVERY_METHOD = (
        ("DHL", "DHL"),
        ("Colissimo", "Colissimo"),
    )

PAYMENT_METHOD = (
        ("Card", "Card"),
        ("Paypal", "Paypal"),
    )
class OrderForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "inputText", "name": "first_name", "placeholder":""}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "inputText", "name": "last_name", "placeholder":""}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "number", "name": "phone"}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={"class": "inputText", "name": "email", "placeholder":""}))
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select(attrs={"class": "country-select", "name": "country", "id":"country"}))    
    address_line_1 = forms.CharField(widget=forms.TextInput(attrs={"class": "", "id":"", "name":"address_line_1"}))
    address_line_1 = forms.CharField(widget=forms.TextInput(attrs={"class": "", "id":"cmyPass", "name":"address_line_2"}))
    postcode = forms.CharField(widget=forms.TextInput(attrs={"class": "", "id":"postcode", "name":"postcode"}))
    city = forms.CharField(widget=forms.TextInput(attrs={"class": "", "id":"city", "name":"city"}))
    zip_code = forms.ChoiceField(choices=ZIP_CHOICES, widget=forms.Select(attrs={"class": "code-phone", "id":"zip_code", "name":"zip_code"}))
    delivery_method = forms.ChoiceField(choices=DELIVERY_METHOD, widget=forms.RadioSelect(attrs={"class": "delivery-method", "name": "delivery_method"}))
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD, widget=forms.RadioSelect(attrs={"class": "payment-method", "name": "payment_method"}))


    class Meta:
        model = Order
        fields = ['first_name', 'zip_code', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2',
                  'country', 'city', 'postcode', 'payment_method', 'delivery_method', 'postcode']
        widgets = {
            'delivery_method': forms.RadioSelect(),
            'payment_method': forms.RadioSelect(),
        }
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        # Si le pays est France, définissez Colissimo comme méthode de livraison par défaut
        if self.instance.country == 'FR':
            self.fields['delivery_method'].initial = 'Colissimo'

        # Cochez les méthodes de paiement et de livraison par défaut
        self.fields['payment_method'].initial = 'Card'
        self.fields['delivery_method'].initial = 'Colissimo'  # Peut-être redondant si déjà défini ci-dessus

        
# class PaymentMethodForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['payment-method']

# class DeriveryMethodForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['derivery-method']