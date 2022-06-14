from django import forms
from .models import Order
class OrderCreateForm(forms.ModelForm):

    email=forms.EmailField()
    first_name=forms.CharField()
    last_name=forms.CharField()
    address=forms.CharField()
    postal_code=forms.CharField()
    city=forms.CharField()

    email.widget.attrs.update({'class':'form-control w-50 '})
    first_name.widget.attrs.update({'class':'form-control w-50'})
    last_name.widget.attrs.update({'class':'form-control w-50'})
    address.widget.attrs.update({'class':'form-control w-50'})
    postal_code.widget.attrs.update({'class':'form-control w-50'})
    city.widget.attrs.update({'class':'form-control w-50'})
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']