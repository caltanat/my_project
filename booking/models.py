from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'client'),
        ('owner', 'owner')
    )
    user_role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='client')
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                                       MaxValueValidator(150)],
                                           null=True, blank=True)


class City(models.Model):
    city = models.CharField(max_length=50)


class Hotel(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=50)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel_description = models.TextField()
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    hotel_stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                                               MaxValueValidator(10)])
    hotel_video = models.FileField(upload_to='hotel_video', null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.hotel_name}, {self.country}, {self.city}'

    def get_average_rating(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_images')
    hotel_image = models.ImageField(upload_to='hotel_image')


class Room(models.Model):
    room_number = models.PositiveSmallIntegerField()
    hotel_room = models.ForeignKey(Hotel, on_delte=models.CASCADE, related_name='rooms')
    TYPE_CHOICES = (
        ('люкс', 'люкс'),
        ('семейный', 'семейный'),
        ('одноместный', 'одноместный'),
        ('двухместный', 'двухместный')
    )
    room_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    STATUS_CHOICES = (
        ('свободен', 'свободен'),
        ('забронирован', 'забронирован'),
        ('занят', 'занят')
)
    room_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='свободен')
    room_price = models.PositiveIntegerField()
    all_inclusive = models.BooleanField(default=False)
    room_description = models.TextField()

    def __str__(self):
        return f'{self.hotel_room} - {self.room_number} - {self.room_type}'



class RoomImagi(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_image = models.ImageField(upload_to='room_image/')


class Review(models.Model):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(null=True, blank=True)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user_name}, {self.hotel} - {self.stars}'

