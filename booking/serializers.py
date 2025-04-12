from rest_framework import serializers
from .models import *


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    room_images = RoomImageSerializer( many=True, read_only=True)
    class Meta:
        model = Room
        fields = [
            'id', 'room_number', 'hotel_room', 'room_type',
            'room_status', 'room_price', 'all_inclusive',
            'room_description', 'room_images'
        ]


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = '__all__'


class HotelSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    hotel_images = HotelImageSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(source='get_average_rating', read_only=True)
    class Meta:
        model = Hotel
        fields = [
            'id', 'city', 'hotel_name', 'owner', 'hotel_description',
            'country', 'hotel_stars', 'hotel_video', 'created_date',
            'average_rating', 'hotel_images', 'rooms'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user_name = UserProfileSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'user_name', 'hotel', 'text', 'stars', 'parent']
