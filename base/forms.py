from django import forms
from .models import LaunchCountdown

class LaunchCountdownForm(forms.ModelForm):
    class Meta:
        model = LaunchCountdown
        fields = ['launch_date',]