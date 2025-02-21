import os
from datetime import date
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from django.db import models
from django.db.models import Max
from django.conf import settings
from django.core.files.storage import default_storage

STATUS_CHOICES = [
    ("available", "Available"),
    ("sold", "Sold"),
]

PROPERTY_TYPE_CHOICES = [
    ("residential", "Residential"),
    ("commercial", "Commercial"),
]

PROPERTY_SUBTYPE_CHOICES = [
    # Residential subtypes
    ("residential_villas/houses", "Residential Villa / Houses"),
    ("residential_apartments", "Residential Apartment"),
    ("residential_land", "Residential Land"),
    ("residential_others", "Residential Other"),

    # Commercial subtypes
    ("commercial_shop", "Commercial Shop"),
    ("commercial_land", "Commercial Land"),
    ("commercial_building", "Commercial Building"),
    ("commercial_others", "Commercial Other"),
]

PLOT_UNIT_CHOICES = [
    ("cent", "Cent"),
    ("acre", "Acre"),
]

class Location(models.Model):
    """
    Model to manage locations manually.
    """
    location_name = models.CharField(max_length=100, unique=True)
    location_image = models.ImageField(upload_to="locations/images/", blank=True, null=True)

    class Meta:
        db_table = "location"
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self) -> str:
        return self.location_name

class Property(models.Model):
    """
    Property model representing a real estate property.
    """
    id = models.AutoField(primary_key=True)
    property_id = models.CharField(
        max_length=10, unique=True, editable=False, blank=True, null=True
    )
    property_name = models.CharField(max_length=50)
    property_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="locations"
    )
    bhk = models.IntegerField(null=True, blank=True)
    square_feet = models.IntegerField(null=True, blank=True)
    possession_date = models.DateField(default=date.today)
    property_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )
    property_description = models.TextField()
    short_description = models.TextField(null=True, blank=True)
    property_main_image = models.ImageField(
        upload_to="properties/images", blank=True, null=True
    )
    gallery_1 = models.ImageField(
        upload_to="properties/images/gallery/", blank=True, null=True
    )
    gallery_2 = models.ImageField(
        upload_to="properties/images/gallery/", blank=True, null=True
    )
    gallery_3 = models.ImageField(
        upload_to="properties/images/gallery/", blank=True, null=True
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    property_subtype = models.CharField(
        max_length=255, choices=PROPERTY_SUBTYPE_CHOICES, default=""
    )
    
    plot_area = models.CharField(
        max_length=50, blank=True, null=True,
        help_text="Specify the plot area."
    )
    plot_unit = models.CharField(
        max_length=10, choices=PLOT_UNIT_CHOICES, blank=True, null=True,
        help_text="Select unit of plot area."
    )
    
    class Meta:
        db_table = "property"

    def __str__(self) -> str:
        return self.property_name

    def is_available(self):
        return self.property_status == "available"

    def display_property_info(self):
        return f"{self.property_name} - {self.property_type} ({self.property_status})"

    def price_per_sqft(self):
        return (
            self.price / self.square_feet
            if self.price and self.square_feet > 0
            else None
        )

    def formatted_price(self):
        if not self.price:
            return "Price not available"

        price = int(self.price)
        if price >= 10**7:
            return f"{price / 10**7:.2f} Crores"
        elif price >= 10**5:
            return f"{price / 10**5:.2f} Lakhs"
        elif price >= 10**3:
            return f"{price / 10**3:.2f} Thousand"
        else:
            return f"{price} Rupees"

    def save(self, *args, **kwargs):
        if not self.property_id:
            last_property = Property.objects.all().aggregate(Max("id"))
            last_property_id = last_property["id__max"]
            self.property_id = f"DL{1000 + (last_property_id or 0)}"
        
        super().save(*args, **kwargs)

        for field in ['property_main_image', 'gallery_1', 'gallery_2', 'gallery_3']:
            image_file = getattr(self, field)
            if image_file:
                self._add_watermark(image_file)

    def _add_watermark(self, image_field):
        image_path = image_field.path
        if not os.path.exists(image_path):
            return

        with Image.open(image_path) as photo:
            watermark_path = os.path.join(settings.BASE_DIR, "static/images/dreamslandrealtys.png")
            watermark = Image.open(watermark_path).convert("RGBA")
            watermark_width = int(photo.width * 1)
            aspect_ratio = watermark.width / watermark.height
            watermark_height = int(watermark_width / aspect_ratio)
            watermark = watermark.resize((watermark_width, watermark_height), Image.Resampling.LANCZOS)
            watermark = watermark.copy()
            alpha = watermark.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(1)
            watermark.putalpha(alpha)
            photo = photo.convert("RGBA")
            position = (
                (photo.width - watermark_width) // 2,
                (photo.height - watermark_height) // 2,
            )
            transparent = Image.new("RGBA", photo.size, (0, 0, 0, 0))
            transparent.paste(photo, (0, 0))
            transparent.paste(watermark, position, mask=watermark)
            final_image = transparent.convert("RGB")
            final_image.save(image_path)
