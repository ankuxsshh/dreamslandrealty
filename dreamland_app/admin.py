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
        # self.fields['square_feet'].required = False  # allow blank in the form
        # if self.instance and self.instance.pk is None:  # only for new objects
        #     self.fields['square_feet'].initial = None  # make it look blank initially

        # self.fields['bhk'].required = False  # allow blank in the form
        # if self.instance and self.instance.pk is None:  # only for new objects
        #     self.fields['bhk'].initial = None  # make it look blank initially


        # if not self.instance.pk:
        #     self.fields['square_feet'].initial = None  # make it look blank initially

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

    # def get_fieldsets(self, request, obj=None):
    #     fieldsets = list(super().get_fieldsets(request, obj))
        
    #     if obj and len(fieldsets) > 1:
    #         fields = []
            
    #         if obj.property_type == 'residential':
    #             if obj.property_subtype == 'residential_land':
    #                 fields = ['plot_area', 'plot_unit']
    #             else:
    #                 fields = ['bhk', 'square_feet', 'possession_date', 'price', 'plot_area', 'plot_unit']
    #         elif obj.property_type == 'commercial':
    #             fields = ['square_feet']
    #         else:
    #             fields = ['bhk', 'square_feet', 'possession_date', 'price', 'plot_area', 'plot_unit']
            
    #         fieldsets[1] = (fieldsets[1][0], {'fields': fields})
        
    #     return fieldsets


    # def get_fieldsets(self, request, obj=None):
    #     fieldsets = list(super().get_fieldsets(request, obj))
        
    #     if obj and len(fieldsets) > 1:
    #         fields = []
    #         existing_fields = list(fieldsets[1][1].get('fields', [])) 
            
    #         if obj.property_type == 'residential':
    #             if obj.property_subtype == 'residential_land':
    #                 fields = ['plot_area', 'plot_unit']
    #                 fields_to_remove = ['bhk', 'square_feet',]
    #             else:
    #                 fields = ['bhk', 'square_feet', 'possession_date', 'price', 'plot_area', 'plot_unit']
    #                 fields_to_remove = []
    #         elif obj.property_type == 'commercial':
    #             fields = ['square_feet']
    #         else:
    #             fields = ['bhk', 'square_feet', 'possession_date', 'price', 'plot_area', 'plot_unit']

    #         updated_fields = [field for field in existing_fields if field not in fields_to_remove]

            
    #         fieldsets[1] = (fieldsets[1][0], {'fields': fields})
        
    #     return fieldsets


    # def get_fieldsets(self, request, obj=None):
    #     fieldsets = super().get_fieldsets(request, obj)

    #     if obj and obj.property_subtype == 'residential_land':
    #         # Find the "Detailed Information" section (2nd section in your case)
    #         detailed_info = fieldsets[1]
    #         section_name, section_options = detailed_info
            
    #         # Remove `bhk` and `square_feet` from the fields list
    #         fields = list(section_options['fields'])
    #         fields = [field for field in fields if field not in ['bhk', 'square_feet']]
            
    #         # Update the fieldset with the modified fields list
    #         fieldsets[1] = (section_name, {'fields': tuple(fields)})

    #     return fieldsets


    # def get_fieldsets(self, request, obj=None):
    #     fieldsets = list(super().get_fieldsets(request, obj))

    #     # Only modify the "Detailed Information" section if we are editing an existing property (not on initial add form).
    #     if obj and len(fieldsets) > 1:
    #         # Base fields for all types
    #         fields = ['price', 'possession_date']

    #         if obj.property_type == 'residential':
    #             if obj.property_subtype == 'residential_land':
    #                 # Residential Land (no BHK and no Square Feet)
    #                 fields.extend(['plot_area', 'plot_unit'])
    #             else:
    #                 # Residential House/Apartment (with BHK and Square Feet)
    #                 fields.extend(['bhk', 'square_feet', 'plot_area', 'plot_unit'])
    #         elif obj.property_type == 'commercial':
    #             # Commercial (usually just Square Feet, can modify if needed)
    #             fields = ['square_feet', 'price', 'possession_date']

    #         # Finally, update the fieldset
    #         fieldsets[1] = ('Detailed Information', {'fields': fields})

    #     return fieldsets



    # def get_fieldsets(self, request, obj=None):
    #     fieldsets = [
    #         ("Basic Information", {
    #             "fields": (
    #                 "property_id", "property_name", "property_location",
    #                 "property_type", "property_subtype",
    #             )
    #         }),
    #         ("Status & Description", {
    #             "fields": ("property_status", "property_description", "short_description"),
    #         }),
    #         ("Gallery", {
    #             "fields": ("property_main_image", "gallery_1", "gallery_2", "gallery_3"),
    #         }),
    #     ]

    #     # Dynamic Detailed Information section
    #     if obj:  # Editing an existing property
    #         if obj.property_subtype == 'residential_land':
    #             detailed_fields = ["price", "plot_area", "plot_unit", "possession_date"]
    #         else:
    #             detailed_fields = ["bhk", "square_feet", "price", "plot_area", "plot_unit", "possession_date"]

    #         fieldsets.insert(1, ("Detailed Information", {"fields": detailed_fields}))

    #     else:  # Adding new property, show all fields by default
    #         detailed_fields = ["bhk", "square_feet", "price", "plot_area", "plot_unit", "possession_date"]
    #         fieldsets.insert(1, ("Detailed Information", {"fields": detailed_fields}))

    #     return fieldsets
