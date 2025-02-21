"""
views.py - This module contains the view functions for the real estate application.
"""

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Property
from datetime import datetime
from django.db.models import Q
from .models import Location
from django.contrib import messages
# from django.core.mail import send_mail
# from django.conf import settings
# from .forms import ContactForm

def index(request):
    """Render the index page with all properties and locations."""
    properties = Property.objects.all()
    locations = Location.objects.all()
    return render(request, "index.html", {"properties": properties, "locations": locations})

def contact(request):
    """Render the contact page."""
    return render(request, "contact.html")


def services(request):
    """Render the services page."""
    return render(request, "services.html")


def career(request):
    """Render the career page."""
    return render(request, "career.html")

def propertieslist(request):
    """Render the propertieslist page."""
    return render(request, "propertieslist.html")


def properties(request):
    """Render the properties page with all properties."""
    properties = Property.objects.all()
    locations = Location.objects.all()
    return render(request, "properties.html", {"properties": properties,"locations": locations})


def about(request):
    """Render the about page."""
    return render(request, "about.html")


def legalteam(request):
    """Render the legal team page."""
    return render(request, "legalteam.html")


def globalreach(request):
    """Render the global reach page."""
    return render(request, "globalreach.html")


def agentsnetwork(request):
    """Render the agents network page."""
    return render(request, "agentsnetwork.html")


# Location dictionary
LOCATIONS = {
    "abu_dhabi": "Abu Dhabi",
    "sharjah": "Sharjah",
    "dubai": "Dubai",
    "umm_al_quwain": "Umm Al Quwain",
    "fujairah": "Fujairah",
    "ajman": "Ajman",
    "ras_al_khaimah": "Ras Al Khaimah",
    "trivandrum": "Trivandrum",
    "alappuzha": "Alappuzha",
    "kottayam": "Kottayam",
    "kochi": "Kochi",
    "thrissur": "Thrissur",
    "kozhikode": "Kozhikode",
    "kannur": "Kannur",
    "mumbai": "Mumbai",
    "pune": "Pune",
    "delhi": "Delhi",
    "noida": "Noida",
    "gurugram": "Gurugram",
    "banglore": "Banglore",
    "hyderabad": "Hyderabad",
    "chennai": "Chennai",
    "kolkata": "Kolkata",
    "ahmedabad": "Ahmedabad",
    "lucknow": "Lucknow",
    "coimbatore": "Coimbatore",
    "goa": "Goa",
    "nagpur": "Nagpur",
    "vancouver": "Vancouver",
}

def get_locations():
    """Fetch the list of unique property locations."""
    return Location.objects.values_list("location_name", flat=True).distinct()

def search_properties(request):
    """Search for properties based on location or property ID using a single input field."""
    locations = Location.objects.all()
    
    # Get the user's search query from a single input field
    search_query = request.GET.get("search", "").strip()
    searched_properties = Property.objects.none()  # Default empty queryset

    if search_query:
        # Try filtering by property ID first
        searched_properties = Property.objects.filter(property_id__icontains=search_query)

        # If no property matches the ID, try filtering by location
        if not searched_properties.exists():
            searched_properties = Property.objects.filter(
                property_location__location_name__icontains=search_query
            )

    context = {
        "locations": locations,
        "search_query": search_query,
        "properties": searched_properties,
        "message": (
            None if searched_properties.exists() else f"No properties found for '{search_query}'."
        ),
    }

    return render(request, "locations.html", context)


def view_location(request, location_slug):
    """Render properties for a specific location."""
    location = get_object_or_404(Location, location_name__iexact=location_slug)
    properties_in_location = Property.objects.filter(property_location=location)

    context = {
        "location": location.location_name,
        "properties": properties_in_location,
        "message": None if properties_in_location.exists() else f"No properties found in {location.location_name}.",
    }

    return render(request, "locations.html", context)


def add_property(request):
    """Add a new property to the database."""
    if request.method == "POST":
        try:
            property_name = request.POST.get("property_name")
            property_location = request.POST.get("property_location")
            bhk = int(request.POST.get("bhk", 0))
            square_feet = int(request.POST.get("square_feet", 0))
            possession_date = datetime.strptime(
                request.POST.get("possession_date"), "%Y-%m-%d"
            )
            property_status = request.POST.get("property_status", "available")
            property_description = request.POST.get("property_description", "")
            short_description = request.POST.get("short_description", "")
            property_type = request.POST.get("property_type", "residential")
            property_subtype = request.POST.get("property_subtype", "villas")
            property_image = request.FILES.get("property_images")

            property_obj = Property(
                property_name=property_name,
                property_location=property_location,
                bhk=bhk,
                square_feet=square_feet,
                possession_date=possession_date,
                property_status=property_status,
                property_description=property_description,
                short_description=short_description,
                property_type=property_type,
                property_subtype=property_subtype,
                property_main_image=property_image,
            )
            property_obj.save()

            return JsonResponse(
                {"status": "success", "message": "Property added successfully!"}
            )
        except ValueError as ve:
            return JsonResponse({"status": "error", "message": str(ve)})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return render(request, "add_property.html")


def property_list(request):
    """Render the list of properties."""
    properties = Property.objects.all()
    return render(request, "property_list.html", {"properties": properties})


def propertydetails(request, property_id):
    """
    Render details for a specific property.
    The images will display with watermark (already handled in the model's save method).
    """
    property_detail = get_object_or_404(Property, pk=property_id)
    return render(request, "propertydetails.html", {"property": property_detail})


def filter_properties(request):
    """Filter properties based on user-selected criteria and display results."""
    print("Received Filters:", request.GET)

    # Extract and clean filters from request
    filters = {
        "location": request.GET.get("location", "").strip(),
        "property_type": request.GET.get("property_type", "").strip(),
        "property_subtype": request.GET.get("property_subtype", "").strip(),
        "bhk": request.GET.get("bhk", "").strip(),
        "min_price": request.GET.get("min_price", 0),
        "max_price": request.GET.get("max_price", 10000000),
        "min_sqft": request.GET.get("min_sqft", 500),
        "max_sqft": request.GET.get("max_sqft", 5000),
    }
    
    # Validate and convert filters to integers if necessary
    try:
        filters["bhk"] = int(filters["bhk"]) if filters["bhk"] else None
        filters["min_price"] = int(filters["min_price"])
        filters["max_price"] = int(filters["max_price"])
        filters["min_sqft"] = int(filters["min_sqft"])
        filters["max_sqft"] = int(filters["max_sqft"])
    except ValueError:
        filters["bhk"] = None
        filters["min_price"] = 0
        filters["max_price"] = 10000000
        filters["min_sqft"] = 500
        filters["max_sqft"] = 5000
    
    # Construct query dynamically
    query = Q()
    if filters["location"]:
        # query &= Q(property_location__location__icontains=filters["location"])
        # query &= Q(property_location__location_name__icontains=filters["location"])
        query &= Q(property_location__location_name__icontains=filters["location"])
    if filters["property_type"]:
        query &= Q(property_type=filters["property_type"])
    if filters["property_subtype"]:
        query &= Q(property_subtype=filters["property_subtype"])
    if filters["bhk"] is not None:
        query &= Q(bhk=filters["bhk"])
    
    # Apply numeric range filters
    query &= Q(price__gte=filters["min_price"], price__lte=filters["max_price"])
    query &= Q(square_feet__gte=filters["min_sqft"], square_feet__lte=filters["max_sqft"])
    
    # Retrieve filtered properties
    properties = Property.objects.filter(query).order_by('price')
    # locations = Location.objects.all()
    
    # Pass context data to template
    context = {
        "properties": properties,
        "selected_filters": filters,
        # "location": Location.objects.all,  # For location autocomplete
        # "locations": locations, 
        # "locations": request.GET.get("location", "").strip(),
    }
    
    return render(request, "propertieslist.html", context)


def add_location(request):
    """
    Add a new location without using forms.py.
    """
    if request.method == "POST":
        location_name = request.POST.get("location_name")
        if location_name:
            # Check if the location already exists
            if Location.objects.filter(location_name=location_name).exists():
                messages.error(request, "Location already exists.")
            else:
                # Save the new location
                Location.objects.create(location_name=location_name)
                messages.success(request, "Location added successfully.")
                return redirect("location_list")
        else:
            messages.error(request, "Location name cannot be empty.")

    return render(request, "index.html")


# def contact_view(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             fullname = form.cleaned_data['fullname']
#             phone = form.cleaned_data['phone']
#             listingtype = form.cleaned_data['listingtype']
#             address = form.cleaned_data['address']

#             # Compose the email message
#             message = f"""
#             Full Name: {fullname}
#             Phone: {phone}
#             Listing Type: {listingtype}
#             Comments: {address}
#             """

#             # Send email to sales@dreamlandrealty.com
#             send_mail(
#                 'Contact Form Submission',
#                 message,
#                 settings.DEFAULT_FROM_EMAIL,  # From email (sales@dreamlandrealty.com)
#                 ['sales@dreamlandrealty.com'],  # To email (recipient)
#                 fail_silently=False,  # Will raise an error if the email sending fails
#             )

#             # Redirect or show a success page after form submission
#             return render(request, 'index.html')  # You can create a thank-you page for confirmation
#     else:
#         form = ContactForm()

#     # Render the contact form for GET requests
#     return render(request, 'index.html', {'form': form})