from django.db import models
from django.contrib.auth.models import User
from produce.models import Crop
from django.conf import settings

# Create your models here.
class Market(models.Model):
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        limit_choices_to={'role__in': ['buyer', 'company']},
        related_name='markets'
    )
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    main_crops = models.ManyToManyField(Crop, related_name='markets', blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    google_maps_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Generate Google Maps link if coordinates are present
        if self.latitude is not None and self.longitude is not None:
            self.google_maps_link = (
                f"https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}"
            )
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.name} ({self.contact_email}) - Buys mainly {self.main_crop_name}"
