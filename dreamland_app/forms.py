from django import forms
from .models import Property, Location

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
        widgets = {
            'property_name': forms.TextInput(attrs={'class': 'form-control'}),
            'property_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'property_location': forms.Select(attrs={'class': 'form-select'}),
            'property_status': forms.Select(attrs={'class': 'form-select'}),
            'bhk': forms.NumberInput(attrs={'class': 'form-control'}),
            'square_feet': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'property_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'property_main_image':  forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'gallery_1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'gallery_2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'gallery_3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'possession_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'plot_area': forms.TextInput(attrs={'class': 'form-control'}),
            'plot_unit': forms.Select(attrs={'class': 'form-select'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'property_subtype': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        locations_queryset = kwargs.pop('locations_queryset', Location.objects.none())
        super(PropertyForm, self).__init__(*args, **kwargs)

        self.fields['property_location'].queryset = locations_queryset
