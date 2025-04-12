from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.contrib import admin


router = DefaultRouter()
router.register(r'userprofile', UserProfileViewSet, basename='user_list'),
router.register(r'hotel', HotelViewSet, basename='hotel'),
router.register(r'room', RoomViewSet, basename='room'),
router.register(r'hotel-image', HotelImageViewSet, basename='hotel-image'),
router.register(r'room-image', RoomImageViewSet, basename='room-image'),
router.register(r'review', ReviewViewSet, basename='review'),
router.register(r'city', CityViewSet, basename='city'),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ru/', include(router.urls)),
]

