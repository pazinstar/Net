# balance/forms.py
from django import forms
from .models import UserBalance


class UserBalanceForm(forms.ModelForm):
    class Meta:
        model = UserBalance
        fields = ['username', 'balance', 'expiry_date']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'balance': forms.NumberInput(attrs={'placeholder': 'Enter balance'}),
            'expiry_date': forms.DateInput(attrs={'placeholder': '2025-05-26'}),
        }
