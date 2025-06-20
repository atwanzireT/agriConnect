# produce/models.py
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db import models
from django.utils.text import slugify

class Crop(models.Model):
    CATEGORY_CHOICES = [
        # Plant-based edible categories
        ('cash_crop', 'Cash Crop'),
        ('cereal', 'Cereal'),
        ('fruit', 'Fruit'),
        ('vegetable', 'Vegetable'),
        ('tuber', 'Tuber'),
        ('legume', 'Legume'),
        ('nut', 'Nut'),
        ('spice', 'Spice'),
        ('herb', 'Herb'),
        ('oil_seed', 'Oil Seed'),
        ('aquatic_plant', 'Aquatic Plant'),
        
        # Animal-based edible categories
        ('livestock', 'Livestock'),  # Cattle, pigs, sheep, goats
        ('poultry', 'Poultry'),  # Chickens, turkeys, ducks
        ('rabbit', 'Rabbit'),  # Domestic rabbits for meat
        ('guinea_pig', 'Guinea Pig'),  # Cuy (common in Andean cuisine)
        ('dairy', 'Dairy'),  # Milk-producing animals
        ('egg_producer', 'Egg Producer'),
        
        # Aquatic edible categories
        ('fish', 'Fish'),
        ('shellfish', 'Shellfish'),
        ('mollusk', 'Mollusk'),
        
        # Other edible categories
        ('game', 'Game'),  # Wild deer, boar, etc.
        ('edible_insect', 'Edible Insect'),
        ('edible_fungus', 'Edible Fungus'),
        
        ('other', 'Other'),
    ]

    name = models.CharField(
        max_length=100, 
        unique=True, 
        help_text="Enter the common name of the edible produce. Example: Maize, Beef, Salmon, Rabbit."
    )
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        help_text="Select the type of edible produce from the list."
    )
    description = models.TextField(
        blank=True, 
        help_text="Describe the edible produce, e.g., nutritional value, culinary uses, or production methods."
    )
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

        
class FarmProduce(models.Model):
    QUALITY_CHOICES = [
        ('top', 'Top Quality (Fresh, No Damage)'),
        ('standard', 'Standard (Minor Defects)'),
        ('fair', 'Fair (Some Damage, Cheaper)'),
    ]

    UNIT_CHOICES = [
        ('kg', 'Kilograms'),
        ('bag', 'Bags (50kg)'),
        ('bunch', 'Bunches'),
        ('piece', 'Pieces'),
    ]

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'farmer'},
        related_name='listings',
        help_text="Your account (auto-selected)."
    )
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, help_text="Type of crop (e.g., maize, beans).")
    variety = models.CharField(max_length=100, help_text="Variety name (e.g., NARO beans, Hybrid maize).")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount available (e.g., 50 kg or 2 bags).")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='kg')
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES, help_text="Select the quality grade.")
    price = models.DecimalField(max_digits=10, decimal_places=0, help_text="Price in Ugandan Shillings (per kg/bag/bunch).")
    available_from = models.DateField(help_text="When will the produce be ready?")
    photo = models.ImageField(upload_to='produce_photos/', help_text="Take a clear photo with your phone.")
    description = models.TextField(blank=True, help_text="Extra details (e.g., organic, storage method).")
    location_lat = models.FloatField(blank=True, null=True, verbose_name="Farm Location (Latitude)")
    location_lng = models.FloatField(blank=True, null=True, verbose_name="Farm Location (Longitude)")
    google_maps_link = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True, help_text="Is this produce still for sale?")
    listed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-listed_at']
        verbose_name = "FarmProduce Listing"
        verbose_name_plural = "FarmProduce Listings"

    def save(self, *args, **kwargs):
        if self.location_lat and self.location_lng:
            self.google_maps_link = f"https://www.google.com/maps?q={self.location_lat},{self.location_lng}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.crop.name} ({self.variety}) by {self.farmer.username}"