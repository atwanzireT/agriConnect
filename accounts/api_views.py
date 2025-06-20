from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import FarmerProfile, BuyerProfile
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    FarmerProfileSerializer,
    BuyerProfileSerializer,
    UserWithFarmerProfileSerializer,
    UserWithBuyerProfileSerializer
)

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class FarmerProfileCreateView(generics.CreateAPIView):
    queryset = FarmerProfile.objects.all()
    serializer_class = FarmerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure user doesn't already have a profile
        if hasattr(self.request.user, 'farmer_profile'):
            raise serializers.ValidationError(_("User already has a farmer profile"))
        
        # Update user role to farmer
        user = self.request.user
        user.role = 'farmer'
        user.save()
        
        serializer.save(user=user)

class FarmerProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = FarmerProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserWithFarmerProfileSerializer
        return FarmerProfileSerializer

    def get_object(self):
        user = self.request.user
        if hasattr(user, 'farmer_profile'):
            return user
        return Response(
            {"detail": "Farmer profile not found."},
            status=status.HTTP_404_NOT_FOUND
        )

class BuyerProfileCreateView(generics.CreateAPIView):
    queryset = BuyerProfile.objects.all()
    serializer_class = BuyerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure user doesn't already have a profile
        if hasattr(self.request.user, 'buyer_profile'):
            raise serializers.ValidationError(_("User already has a buyer profile"))
        
        # Update user role to buyer
        user = self.request.user
        user.role = 'buyer'
        user.save()
        
        serializer.save(user=user)

class BuyerProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = BuyerProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserWithBuyerProfileSerializer
        return BuyerProfileSerializer

    def get_object(self):
        user = self.request.user
        if hasattr(user, 'buyer_profile'):
            return user
        return Response(
            {"detail": "Buyer profile not found."},
            status=status.HTTP_404_NOT_FOUND
        )