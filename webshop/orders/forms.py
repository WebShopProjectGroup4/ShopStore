from django import forms
from .models import Order
class OrderCreateForm(forms.ModelForm):

    
    email=forms.EmailField()
    first_name=forms.CharField()
    last_name=forms.CharField()
    address=forms.CharField()
    postal_code=forms.CharField()
    city=forms.CharField()

    email.widget.attrs.update({'class':'form-control'})
    first_name.widget.attrs.update({'class':'form-control'})
    last_name.widget.attrs.update({'class':'form-control'})
    address.widget.attrs.update({'class':'form-control'})
    postal_code.widget.attrs.update({'class':'form-control'})
    city.widget.attrs.update({'class':'form-control'})

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']