"""
views.py - This module contains the view functions for the real estate application.
"""

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Property
from datetime import datetime
from django.db.models import Q
from .models import Location
from django.contrib import messages


def index(request):
    """Render the index page with all properties and locations in ascending order."""
    properties = Property.objects.all()
    locations = Location.objects.all().order_by("location_name")  # Order locations alphabetically
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
    """Render the index page with all properties and locations in ascending order."""
    properties = Property.objects.all()
    locations = Location.objects.all().order_by("location_name")  # Order locations alphabetically
    return render(request, "properties.html",  {"properties": properties, "locations": locations})

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


def propertydetails(request, property_id):
    """
    Render details for a specific property.
    The images will display with watermark (already handled in the model's save method).
    """
    property_detail = get_object_or_404(Property, pk=property_id)
    return render(request, "propertydetails.html", {"property": property_detail})

def filter_properties(request):
    """Filter properties based on user-selected criteria and display results."""
    print("Starting filter_properties function...")

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

    # Debugging: Print out the filters before processing
    print(f"Extracted filters: {filters}")

    # Validate and convert filters to integers if necessary
    try:
        filters["bhk"] = int(filters["bhk"]) if filters["bhk"] else None
        filters["min_price"] = int(filters["min_price"])
        filters["max_price"] = int(filters["max_price"])
        filters["min_sqft"] = int(filters["min_sqft"])
        filters["max_sqft"] = int(filters["max_sqft"])
    except ValueError as e:
        print(f"Error in converting filter values: {e}")
        filters["bhk"] = None
        filters["min_price"] = 0
        filters["max_price"] = 10000000
        filters["min_sqft"] = 500
        filters["max_sqft"] = 5000
    
    # Debugging: Print out filters after validation and conversion
    print(f"Validated filters: {filters}")

    # Construct query dynamically
    query = Q()

    # Location filter (assuming location is a ForeignKey in Property model)
    if filters["location"]:
        print(f"Adding location filter: {filters['location']}")
        query &= Q(property_location__icontains=filters["location"])

    # Property type filter
    if filters["property_type"]:
        print(f"Adding property_type filter: {filters['property_type']}")
        query &= Q(property_type=filters["property_type"])

    # Property subtype filter
    if filters["property_subtype"]:
        print(f"Adding property_subtype filter: {filters['property_subtype']}")
        query &= Q(property_subtype=filters["property_subtype"])

    # BHK filter
    if filters["bhk"] is not None:
        print(f"Adding BHK filter: {filters['bhk']}")
        query &= Q(bhk=filters["bhk"])
    
    # Price range filter
    print(f"Adding price filter: {filters['min_price']} - {filters['max_price']}")
    query &= Q(price__gte=filters["min_price"], price__lte=filters["max_price"])

    # Square footage range filter
    print(f"Adding sqft filter: {filters['min_sqft']} - {filters['max_sqft']}")
    query &= Q(square_feet__gte=filters["min_sqft"], square_feet__lte=filters["max_sqft"])

    # Debugging: Print out the query being executed
    print(f"Final query: {query}")

    # Retrieve filtered properties
    try:
        properties = Property.objects.filter(query).order_by('price')
        print(f"Fetched {len(properties)} properties.")
    except Exception as e:
        print(f"Error fetching properties: {e}")
        return HttpResponse(f"Error fetching properties: {e}", status=500)

    # Pass context data to template
    context = {
        "properties": properties,
        "selected_filters": filters,
        "locations": Location.objects.all(),  # For location autocomplete or listing
    }

    print("Rendering template with filtered properties...")

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