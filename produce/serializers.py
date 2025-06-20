# produce/serializers.py
from rest_framework import serializers
from .models import Crop, FarmProduce
from django.conf import settings

class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'
        read_only_fields = ('slug',)

    def validate_name(self, value):
        """Ensure name is title case for consistency"""
        return value.title()

class FarmProduceSerializer(serializers.ModelSerializer):
    farmer_name = serializers.CharField(source='farmer.get_full_name', read_only=True)
    farmer_phone = serializers.CharField(source='farmer.phone_number', read_only=True)
    crop_name = serializers.CharField(source='crop.name', read_only=True)
    crop_category = serializers.CharField(source='crop.category', read_only=True)
    
    class Meta:
        model = FarmProduce
        fields = '__all__'
        read_only_fields = ('google_maps_link', 'listed_at', 'slug')
    
    def validate_price(self, value):
        """Ensure price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        return value
    
    def validate_quantity(self, value):
        """Ensure quantity is positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero")
        return value

class FarmProduceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmProduce
        fields = [
            'crop', 'variety', 'quantity', 'unit', 'quality', 
            'price', 'available_from', 'photo', 'description',
            'location_lat', 'location_lng', 'is_available'
        ]
    
    def create(self, validated_data):
        """Automatically set the farmer to the current user"""
        validated_data['farmer'] = self.context['request'].user
        return super().create(validated_data)

class CropWithProduceSerializer(serializers.ModelSerializer):
    """Serializer for Crop that includes related produce listings"""
    produce_listings = serializers.SerializerMethodField()
    
    class Meta:
        model = Crop
        fields = ['id', 'name', 'category', 'description', 'slug', 'produce_listings']
    
    def get_produce_listings(self, obj):
        """Get active produce listings for this crop"""
        listings = obj.produce.filter(is_available=True)
        return FarmProduceSerializer(listings, many=True).data