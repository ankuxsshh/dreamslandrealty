# from django import forms

# class ContactForm(forms.Form):
#     fullname = forms.CharField(label='Full Name', max_length=100)
#     phone = forms.CharField(label='Phone Number', max_length=15)
#     listingtype = forms.ChoiceField(label='Listing Type', choices=[('Seller', 'Seller'), ('Buyer', 'Buyer')])
#     address = forms.CharField(label='Comments', widget=forms.Textarea, max_length=500)


# from django import forms
# from .models import Property, Location

# class PropertyForm(forms.ModelForm):
#     class Meta:
#         model = Property
#         fields = '__all__'
#         widgets = {
#             'property_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'property_price': forms.NumberInput(attrs={'class': 'form-control'}),
#             'property_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
#             'property_location': forms.Select(attrs={'class': 'form-select'}),  # Bootstrap 5 uses form-select
#             'property_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }

#     def __init__(self, *args, **kwargs):
#         locations_queryset = kwargs.pop('locations_queryset', Location.objects.none())
#         super(PropertyForm, self).__init__(*args, **kwargs)

#         self.fields['property_location'] = forms.ModelChoiceField(
#             queryset=locations_queryset,
#             required=True,
#             label="Property Location",
#             widget=forms.Select(attrs={'class': 'form-select'})  # For dropdowns
#         )



# from django import forms
# from .models import Property, Location

# class PropertyForm(forms.ModelForm):
#     class Meta:
#         model = Property
#         fields = '__all__'

#         widgets = {
#             'property_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'property_price': forms.NumberInput(attrs={'class': 'form-control'}),
#             'property_description': forms.Textarea(attrs={'class': 'form-control'}),
#             'property_location': forms.Select(attrs={'class': 'form-control'}),
#             'property_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
#         }

#     def __init__(self, *args, **kwargs):
#         locations_queryset = kwargs.pop('locations_queryset', Location.objects.none())
#         super(PropertyForm, self).__init__(*args, **kwargs)

#         # Filter property_location field
#         self.fields['property_location'] = forms.ModelChoiceField(
#             queryset=locations_queryset,
#             required=True,
#             label="Property Location",
#              widget=forms.Select(attrs={'class': 'form-control'})  # Add class here too
#         )

from django import forms
from .models import Property, Location

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        locations_queryset = kwargs.pop('locations_queryset', Location.objects.none())
        super(PropertyForm, self).__init__(*args, **kwargs)

        # Filter property_location field
        self.fields['property_location'] = forms.ModelChoiceField(
            queryset=locations_queryset,
            required=True,
            label="Property Location"
        )