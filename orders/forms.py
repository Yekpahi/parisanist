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
    delivery_method = forms.ChoiceField(choices=DELIVERY_METHOD, widget=forms.RadioSelect(attrs={"name": "delivery_method", "class": "delivery_method_inputs"}))
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD, widget=forms.RadioSelect(attrs={"name": "payment_method", "class": "payment_method_inputs"}))

    class Meta:
        model = Order
        fields = ['first_name', 'zip_code', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2',
                  'country', 'city', 'postcode', 'payment_method', 'delivery_method', 'postcode']
        widgets = {
            'delivery_method': forms.RadioSelect(),
            'payment_method': forms.RadioSelect(),
        }
    def __init__(self, *args, **kwargs):
        user_country = kwargs.pop('user_country', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        
        # Modifier les choix disponibles pour delivery_method en fonction du pays de l'utilisateur
        if user_country == 'FR':
            self.fields['delivery_method'].choices = [('Colissimo', 'Colissimo')]
            self.fields['delivery_method'].initial = 'Colissimo'
            self.fields['payment_method'].initial = 'Card'

        else:
            # Assumez ici vos autres options de livraison par défaut
            self.fields['delivery_method'].choices = [('DHL', 'DHL')]
            self.fields['delivery_method'].initial = 'DHL'
            self.fields['payment_method'].initial = 'Card'

        