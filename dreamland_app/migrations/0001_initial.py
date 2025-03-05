"""
0001_initial.py - This module contains the initial migration for the dreamland_app.
"""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Migration to create the initial database schema for the dreamland_app.
    """

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Property",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("property_name", models.CharField(max_length=255)),
                ("property_location", models.CharField(max_length=255)),
                ("bhk", models.IntegerField()),
                ("square_feet", models.IntegerField()),
                ("possession_date", models.DateField()),
                ("property_status", models.CharField(max_length=20)),
                ("property_description", models.TextField()),
                ("short_description", models.TextField(blank=True, null=True)),
                (
                    "property_main_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="properties/images"
                    ),
                ),
                (
                    "gallery_images",
                    models.ImageField(
                        blank=True, null=True, upload_to="properties/images/gallery/"
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("property_type", models.CharField(max_length=50)),
                ("property_subtype", models.CharField(default="", max_length=255)),
            ],
        ),
    ]
