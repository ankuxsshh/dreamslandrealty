from django.contrib import admin
from .models import Property, Location, Agent
from django.contrib.auth.models import Group, User
from django import forms
from django.utils.translation import gettext_lazy as _

admin.site.unregister(Group)
admin.site.unregister(User)

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Location, Property, Agent

class AgentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "agent_id", "district_place", "contact_number")
    search_fields = ("first_name", "last_name", "agent_id", "district_place")
    filter_horizontal = ("allocated_locations",)  # Enable multi-select for locations

    readonly_fields = ("agent_id",)  # Display but not allow editing

    fieldsets = (
        (_("Basic Information"), {
            "fields": ("first_name", "last_name", "username", "password"),
            "classes": ("collapse",),
        }),
        (_("Personal Information"), {
            "fields": ("personal_address", "district_place", "age", "contact_number", "whatsapp_number"),
            "classes": ("collapse",),
        }),
        (_("Allocated Locations"), {
            "fields": ("allocated_locations",),
            "classes": ("collapse",),
        }),
    )

admin.site.register(Agent, AgentAdmin)


class PropertyAdminForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    # class Media:
    #     js = ('js/property_form.js',)

    list_display = (
        "property_id", "property_name", "property_type", "property_subtype",
        "property_status", "price",
    )
    list_filter = ("property_type", "property_status", "property_subtype")
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