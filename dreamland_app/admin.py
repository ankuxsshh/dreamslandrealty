from django.contrib import admin
from .models import Property, Location
from django.contrib.auth.models import Group
from django import forms

admin.site.unregister(Group)

class PropertyAdminForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically update property_subtype choices based on property_type
        if 'property_type' in self.data:
            property_type = self.data.get('property_type')
        elif self.instance and self.instance.pk:
            property_type = self.instance.property_type
        else:
            property_type = None

        if property_type == 'residential':
            self.fields['property_subtype'].choices = [
                ('residential_villas/houses', 'Residential Villas/Houses'),
                ('residential_apartments', 'Residential Apartments'),
                ('residential_land', 'Residential Land'),
                ('residential_others', 'Residential Other'),
            ]
        elif property_type == 'commercial':
            self.fields['property_subtype'].choices = [
                ('commercial_shop', 'Commercial Shops'),
                ('commercial_land', 'Commercial Land'),
                ('commercial_building', 'Commercial Buildings'),
                ('commercial_others', 'Commercial Other'),
            ]

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "location_name")
    search_fields = ("location_name",)
    ordering = ("location_name",)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    form = PropertyAdminForm

    list_display = (
        "property_id", "property_name", "property_type", "property_subtype",
        "property_status", "price",
    )
    list_filter = ("property_type", "property_status")
    search_fields = ("property_name", "property_location__location_name")
    ordering = ("property_name",)
    readonly_fields = ("property_id",)

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "property_id", "property_name", "property_location",
                "property_type", "property_subtype",
            )
        }),
        ("Detailed Information", {
            "fields": ("bhk", "square_feet", "price", "plot_area", "plot_unit", "possession_date",),
        }),
        ("Status & Description", {
            "fields": ("property_status", "property_description", "short_description"),
        }),
        ("Gallery", {
            "fields": ("property_main_image", "gallery_1", "gallery_2", "gallery_3"),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

def get_fieldsets(self, request, obj=None):
    fieldsets = list(super().get_fieldsets(request, obj))
    
    if obj and len(fieldsets) > 1:
        fields = []
        
        if obj.property_type == 'residential':
            if obj.property_subtype == 'residential_land':
                fields = ['plot_area', 'plot_unit']
            else:
                fields = ['bhk', 'square_feet', 'possession_date', 'price', 'plot_area', 'plot_unit']
        elif obj.property_type == 'commercial':
            fields = ['square_feet']
        else:
            fields = ['bhk', 'square_feet', 'possession_date', 'price', 'plot_area', 'plot_unit']
        
        fieldsets[1] = (fieldsets[1][0], {'fields': fields})
    
    return fieldsets
