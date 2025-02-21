"""
apps.py - This module configures the Django application for the real estate project.
"""

from django.apps import AppConfig


class RealAppConfig(AppConfig):
    """
    Configuration class for the RealApp application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "dreamland_app"
