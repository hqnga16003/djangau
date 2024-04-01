from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField

# Create your models here.
from django.db.transaction import on_commit


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True)


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['id']


class Location(BaseModel):
    name = models.CharField(max_length=50)


class Category(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# chuyen xe


# tuyen xe
class Buses(BaseModel):
    id_departure_point = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="departure_routes")
    id_arrival_point = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="arrival_routes")
    active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DurationField()


class Drivers(BaseModel):
    name = models.CharField(max_length=50)


class Staff(BaseModel):
    name = models.CharField(max_length=50)


class Customer(BaseModel):
    name = models.CharField(max_length=50)


# chuyen xe
class Trips(BaseModel):
    bus = models.ForeignKey(Buses, on_delete=models.CASCADE, related_name="trips")
    driver = models.ForeignKey(Drivers, on_delete=models.CASCADE, related_name="trips")
    departure_date = models.DateField()
    departure_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = (("bus", "departure_date", "departure_time"),)


# ve xe
class Ticket(BaseModel):
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE, related_name="tickets")
    customer_name = models.CharField(max_length=255)  # Consider using a Customer model for details
    quantity_ticket = models.PositiveIntegerField()  # Ensures positive number of tickets
    price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateField()

class FeedBack(BaseModel):
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE, related_name="feedback")
    customer_name = models.CharField(max_length=255)  # Consider using a Customer model for details
    content = models.TextField()
    rating = models.IntegerField(choices=((1, "Poor"), (2, "Fair"), (3, "Good"), (4, "Very Good"), (5, "Excellent")))

