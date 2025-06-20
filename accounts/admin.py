from django.contrib import admin
from .models import User, FarmerProfile, BuyerProfile

# Register your models here.
admin.site.register(User)
admin.site.register(FarmerProfile)
admin.site.register(BuyerProfile)