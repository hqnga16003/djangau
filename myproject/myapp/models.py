from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField

# Create your models here.
from django.db.transaction import on_commit


class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['id']


class Location(BaseModel):
    name = models.CharField(max_length=50)


# class Category(BaseModel):
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name


class BusRoute(models.Model):
    departure_point = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="departure_buses")
    arrival_point = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="arrival_buses")
    is_active = models.BooleanField(default=True)  # Clearer variable name
    price = models.DecimalField(max_digits=10, decimal_places=2)
    departure_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.departure_point} -> {self.arrival_point} (Price: ${self.price:.2f})"

    class Meta:
        verbose_name = "Bus Route"
        verbose_name_plural = "Bus Routes"


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True)
    user_type = models.CharField(max_length=20, choices=(
        ('driver', 'Driver'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ), default='customer')


# chuyen xe
class BusSchedule(models.Model):

    bus = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name="schedules")
    assigned_driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                        related_name="assigned_schedules")
    departure_date = models.DateField()
    departure_time = models.TimeField()
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = (("bus", "departure_date", "departure_time"),)

    def __str__(self):
        return f"{self.bus}: {self.departure_date} {self.departure_time} ({self.assigned_driver} - ${self.price_per_seat:.2f})"  # Informative string representation


# ve xe

class Booking(models.Model):
    scheduled_trip = models.ForeignKey(BusSchedule, on_delete=models.CASCADE,
                                       related_name="bookings")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    number_of_seats = models.PositiveIntegerField(
        validators=[MaxValueValidator(10)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.scheduled_trip} ({self.number_of_seats} seats - ${self.total_price:.2f})"


class CustomerReview(models.Model):

    reviewed_trip = models.ForeignKey(BusSchedule, on_delete=models.CASCADE,
                                      related_name="reviews")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    review_text = models.TextField()
    rating = models.IntegerField(choices=((1, "Poor"), (2, "Fair"), (3, "Good"), (4, "Very Good"), (5, "Excellent")))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} reviewed {self.reviewed_trip} ({self.rating}): {self.review_text[:50]}..."
