from django.contrib import admin
from .models import FarmProduce, Crop

# Register your models here.
admin.site.register(Crop)
admin.site.register(FarmProduce)