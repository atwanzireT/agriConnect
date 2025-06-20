from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FarmerProfile, BuyerProfile
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'phone_number', 'location', 'verified', 'preferred_language']
        read_only_fields = ['id', 'verified', 'role']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'phone_number', 'location', 'preferred_language']
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(_("Passwords don't match"))
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        # Default role is guest, can be updated when creating profile
        validated_data['role'] = 'guest'
        user = User.objects.create_user(**validated_data)
        return user

class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = '__all__'
        read_only_fields = ['user']
        extra_kwargs = {
            'group_name': {'required': False},
            'farm_size': {'required': False},
        }

    def validate(self, data):
        if data.get('is_group') and not data.get('group_name'):
            raise serializers.ValidationError(_("Group name is required for farmer groups"))
        elif not data.get('is_group') and not data.get('farm_size'):
            raise serializers.ValidationError(_("Farm size is required for individual farmers"))
        return data

class BuyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = '__all__'
        read_only_fields = ['user']

class UserWithFarmerProfileSerializer(serializers.ModelSerializer):
    farmer_profile = FarmerProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'phone_number', 'location', 'verified', 'preferred_language', 'farmer_profile']

class UserWithBuyerProfileSerializer(serializers.ModelSerializer):
    buyer_profile = BuyerProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'phone_number', 'location', 'verified', 'preferred_language', 'buyer_profile']