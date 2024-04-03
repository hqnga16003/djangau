from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField

# Create your models here.
from django.db.transaction import on_commit
from rest_framework.exceptions import ValidationError


class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['id']


class Location(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True)
    user_type = models.CharField(max_length=20, choices=(
        ('driver', 'Driver'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ), default='customer')


class Bus(models.Model):
    license_plate = models.CharField(max_length=50, unique=True)
    total_seats = models.PositiveIntegerField(default=40)

    def __str__(self):
        return f"{self.license_plate}"


class BusRoute(models.Model):
    departure_point = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="departure_buses")
    arrival_point = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="arrival_buses")
    is_active = models.BooleanField(default=True)  # Clearer variable name
    price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_travel_time = models.PositiveIntegerField(blank=True, null=True)

    def clean_fields(self, *args, **kwargs):
        if self.departure_point == self.arrival_point:
            raise ValidationError("Departure and arrival points cannot be the same.")

        super().clean_fields()

    def __str__(self):
        return f"{self.departure_point} -> {self.arrival_point} "

    class Meta:
        verbose_name = "Bus Route"
        verbose_name_plural = "Bus Routes"
        unique_together = (("departure_point", "arrival_point"),)

    def get_price(self):
        return self.price



class BusSchedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="bus_schedules")
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name="route_schedules")
    assigned_driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                        related_name="assigned_schedules")
    departure_date = models.DateField()
    departure_time = models.TimeField()
    surcharge = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    number_of_seats_booked = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.bus}: {self.bus_route}"

    class Meta:
        unique_together = (("bus", "departure_date", "departure_time"),)

    def is_seat_available(self):
        return self.bus.get_seats() > self.number_of_seats_booked

    def book_seat(self):
        if self.is_seat_available():
            self.number_of_seats_booked += 1
            self.save()
            return True
        return False

    def cancel_seat_booking(self):
        if self.number_of_seats_booked > 0:
            self.number_of_seats_booked -= 1
            self.save()
            return True
        return False

    def get_price(self):
        return self.bus_route.get_price() + self.surcharge



class Booking(models.Model):
    bus_schedule = models.ForeignKey(BusSchedule, on_delete=models.CASCADE,
                                     related_name="bookings")
    sales_staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="sales_bookings")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    is_active = models.BooleanField(default=True)  # Clearer variable name
    created_at = models.DateTimeField(auto_now_add=True)
    total_seats = models.PositiveIntegerField(default=1)


class Seat(models.Model):
    number_seat = models.IntegerField()
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="seats")


class CustomerReview(models.Model):
    reviewed_trip = models.ForeignKey(BusSchedule, on_delete=models.CASCADE,
                                      related_name="reviews")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    review_text = models.TextField()
    rating = models.IntegerField(choices=((1, "Poor"), (2, "Fair"), (3, "Good"), (4, "Very Good"), (5, "Excellent")))
    created_at = models.DateTimeField(auto_now_add=True)