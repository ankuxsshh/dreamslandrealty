from django.urls import path
from . import views
from .views import send_whatsapp

urlpatterns = [
    path("", views.index, name="index"),
    path("contact", views.contact, name="contact"),
    path("services", views.services, name="services"),
    path("career", views.career, name="career"),
    path("properties", views.properties, name="properties"),
    path("propertieslist", views.propertieslist, name="propertieslist"),
    path("about", views.about, name="about"),
    path("legalteam", views.legalteam, name="legalteam"),
    path("globalreach", views.globalreach, name="globalreach"),
    path("agentsnetwork", views.agentsnetwork, name="agentsnetwork"),
    path("location/<slug:location_slug>/", views.view_location, name="view_location"),
    path(
        "propertydetails/<int:property_id>",
        views.propertydetails,
        name="propertydetails",
    ),
    path("search", views.search_properties, name="search_properties"),
    path("propertieslist/", views.filter_properties, name="filter_properties"),
    path("locations/add/", views.add_location, name="add_location"),
    path('send_whatsapp/', send_whatsapp, name='send_whatsapp'),
    

    path('agent-login/', views.agent_login, name='agent_login'),
    path('agent-dashboard', views.agent_dashboard, name='agent_dashboard'),
    path('agent-logout/', views.agent_logout, name='agent_logout'),
    path('agent/add-property/', views.add_property_agent, name='add_property_agent'),
    path('agent/edit-property/<int:property_id>/', views.edit_property, name='edit_property'),
    path('agent/delete-property/<int:property_id>/', views.delete_property, name='delete_property'),
]
