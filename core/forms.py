from django import forms
from core.models import CreditCard

class CreditCardForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Card Holder Name"}))
    # number = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder":"Card Number"}))
    # month = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder":"Expiry Month"}))
    # year = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder":"Card Year"}))
    # cvv = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder":"CVV"}))
    
    class Meta:
        model = CreditCard
        fields = ['name', 'number', 'month', 'year', 'cvv', 'card_type']
        widgets = {
            "name": forms.TextInput(attrs={"placeholder":"Card Holder Name"}),
            "number": forms.TextInput(attrs={"placeholder":"Card Number"}),
            "month": forms.TextInput(attrs={"placeholder":"Expiry Month"}),
            "year": forms.TextInput(attrs={"placeholder":"Card Year"}),
            "cvv": forms.TextInput(attrs={"placeholder":"CVV"}),
        }