from django.urls import path
from .api_views import (
    UserRegistrationView,
    UserDetailView,
    FarmerProfileCreateView,
    FarmerProfileDetailView,
    BuyerProfileCreateView,
    BuyerProfileDetailView
)

urlpatterns = [
    # User endpoints
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    
    # Farmer profile endpoints
    path('profiles/farmer/', FarmerProfileCreateView.as_view(), name='farmer-profile-create'),
    path('profiles/farmer/me/', FarmerProfileDetailView.as_view(), name='farmer-profile-detail'),
    
    # Buyer profile endpoints
    path('profiles/buyer/', BuyerProfileCreateView.as_view(), name='buyer-profile-create'),
    path('profiles/buyer/me/', BuyerProfileDetailView.as_view(), name='buyer-profile-detail'),
]