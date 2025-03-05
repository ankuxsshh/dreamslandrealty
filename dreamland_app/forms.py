# from django import forms

# class ContactForm(forms.Form):
#     fullname = forms.CharField(label='Full Name', max_length=100)
#     phone = forms.CharField(label='Phone Number', max_length=15)
#     listingtype = forms.ChoiceField(label='Listing Type', choices=[('Seller', 'Seller'), ('Buyer', 'Buyer')])
#     address = forms.CharField(label='Comments', widget=forms.Textarea, max_length=500)


from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['property_id']