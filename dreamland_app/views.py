"""
views.py - This module contains the view functions for the real estate application.
"""

from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Property, Agent
from datetime import datetime
from django.db.models import Q
from .models import Location
from django.contrib import messages
from datetime import date
from django.http import JsonResponse
import urllib.parse

from django.contrib.auth import logout
from .forms import PropertyForm


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
    print("Received Filters:", request.GET)

    # Extract and clean filters from request
    filters = {
        "location": request.GET.get("location", "").strip(),
        "property_type": request.GET.get("property_type", "").strip(),
        "property_subtype": request.GET.get("property_subtype", "").strip(),
        "bhk": request.GET.get("bhk", "").strip(),
        "min_price": request.GET.get("min_price", 0),
        "max_price": request.GET.get("max_price", 10000000),
        "min_sqft": request.GET.get("min_sqft", "500"),
        "max_sqft": request.GET.get("max_sqft", "5000"),
    }

    print("Filters before processing:", filters)
    
    # Validate and convert filters to integers if necessary
    try:
        # filters["bhk"] = int(filters["bhk"]) if filters["bhk"] else None
        if filters["bhk"] and filters["bhk"].lower() != "null":  # Check if "bhk" is valid
            filters["bhk"] = int(filters["bhk"])  
        else:  
            filters.pop("bhk", None)  # Remove "bhk" if it's empty, "null", or invalid
        filters["min_price"] = int(filters["min_price"])
        filters["max_price"] = int(filters["max_price"])
        # filters["min_sqft"] = int(filters["min_sqft"])
        # filters["max_sqft"] = int(filters["max_sqft"])
        if filters["min_sqft"] and filters["min_sqft"].lower() != "null":  # Check if "min_sqft" is valid
            filters["min_sqft"] = int(filters["min_sqft"])  
        else:  
            filters.pop("min_sqft", None)  # Remove "min_sqft" if it's empty, "null", or invalid

        if filters["max_sqft"] and filters["max_sqft"].lower() != "null":  # Check if "max_sqft" is valid
            filters["max_sqft"] = int(filters["max_sqft"])  
        else:  
            filters.pop("max_sqft", None)  # Remove "max_sqft" if it's empty, "null", or invalid

    except ValueError:
        # filters["bhk"] = None
        filters.pop("bhk", None)
        filters["min_price"] = 0
        filters["max_price"] = 10000000
        # filters["min_sqft"] = 500
        # filters["max_sqft"] = 5000
        filters.pop("min_sqft", None)
        filters.pop("max_sqft", None)

    print("Filters after processing:", filters)
    
    # Construct query dynamically
    query = Q()
    if filters["location"]:
        query &= Q(property_location__location_name__icontains=filters["location"])
    if filters["property_type"]:
        query &= Q(property_type=filters["property_type"])
    if filters["property_subtype"]:
        query &= Q(property_subtype=filters["property_subtype"])
    # if filters["bhk"] is not None:
    #     query &= Q(bhk=filters["bhk"])
    if "bhk" in filters:
        query &= (Q(bhk=filters["bhk"]) | Q(bhk__isnull=True))  # Include properties with no bhk value
    
    # Apply numeric range filters
    query &= Q(price__gte=filters["min_price"], price__lte=filters["max_price"])
    # query &= Q(square_feet__gte=filters["min_sqft"], square_feet__lte=filters["max_sqft"])
    
    sqft_query = Q()

    if "min_sqft" in filters and "max_sqft" in filters:
        sqft_query |= Q(square_feet__gte=filters["min_sqft"], square_feet__lte=filters["max_sqft"])
        sqft_query |= Q(square_feet__isnull=True)  # Allow properties with NULL square feet (no value)

    query &= sqft_query
    
    # Retrieve filtered properties
    properties = Property.objects.filter(query).order_by('price')
    # locations = Location.objects.all()

    print("Final Query:", query)
    
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

def agent_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            agent = Agent.objects.get(username=username, password=password)  # Normally you should hash passwords
            request.session['agent_id'] = agent.id  # Store agent in session
            return redirect('agent_dashboard')
        except Agent.DoesNotExist:
            messages.error(request, "Invalid credentials.")
    return render(request, 'agent_login.html')


def get_logged_in_agent(request):
    agent_id = request.session.get('agent_id')
    if not agent_id:
        return None
    return Agent.objects.get(id=agent_id)

def agent_dashboard(request):
    agent = get_logged_in_agent(request)
    if not agent:
        return redirect('agent_login')
    
    # Fetch properties only in the agent's locations
    properties = Property.objects.filter(property_location__in=agent.allocated_locations.all())
    return render(request, 'agent_dashboard.html', {'properties': properties})



def add_property_agent(request):
    agent = get_logged_in_agent(request)
    if not agent:
        return redirect('agent_login')

    # Fetch only allocated locations for this agent
    allocated_locations = agent.allocated_locations.all()

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, locations_queryset=allocated_locations)
        if form.is_valid():
            property = form.save(commit=False)

            # Assign location automatically if the agent has only one allocated location
            if allocated_locations.count() == 1:
                property.property_location = allocated_locations.first()

            property.save()
            return redirect('agent_dashboard')
    else:
        form = PropertyForm(locations_queryset=allocated_locations)

        # Pre-set and disable location if agent has only one location
        if allocated_locations.count() == 1:
            form.fields['property_location'].initial = allocated_locations.first()
            # form.fields['property_location'].disabled = True

    return render(request, 'property_form.html', {'form': form})


def edit_property(request, property_id):
    agent = get_logged_in_agent(request)
    if not agent:
        return redirect('agent_login')

    property = get_object_or_404(Property, id=property_id)

    # Ensure agent can only edit properties in their locations
    if property.property_location not in agent.allocated_locations.all():
        return HttpResponseForbidden("You are not allowed to edit this property.")

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            return redirect('agent_dashboard')
    else:
        form = PropertyForm(instance=property)

    form.fields['property_location'].disabled = True  # Disable location editing
    return render(request, 'property_form.html', {'form': form})

def delete_property(request, property_id):
    agent = get_logged_in_agent(request)
    if not agent:
        return redirect('agent_login')

    property = get_object_or_404(Property, id=property_id)

    # Security Check - Ensure agent can only delete properties from their own locations
    if property.property_location not in agent.allocated_locations.all():
        return HttpResponseForbidden("You are not allowed to delete this property.")

    property.delete()
    return redirect('agent_dashboard')

def agent_logout(request):
    logout(request)
    request.session.flush()
    return redirect('agent_login')


def send_whatsapp(request):
    property_id = request.GET.get('property_id')
    
    if not property_id:
        return JsonResponse({"success": False, "error": "Property ID is missing"})
    
    property_obj = get_object_or_404(Property, property_id=property_id)
    
    message = f"Hello, I'm interested in this Property :\nName : {property_obj.property_name}\nPrice : {property_obj.formatted_price()}\nLocation : {property_obj.property_location}\nPlease provide more details."
    
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/+916238061066?text={encoded_message}"
    
    return JsonResponse({"success": True, "whatsapp_url": whatsapp_url})