from datetime import datetime, timedelta

from cloudinary.templatetags import cloudinary
from cloudinary.uploader import upload
from django.contrib.auth.hashers import make_password
from django.core.validators import MaxValueValidator, MinValueValidator
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
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = CloudinaryField('avatar', null=True)
    user_type = models.CharField(max_length=20, choices=(
        ('driver', 'Driver'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ), default='customer')

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Bus(models.Model):
    license_plate = models.CharField(max_length=50, unique=True)
    total_seats = models.PositiveIntegerField(default=40)
    driver = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'user_type': 'driver'})

    def get_total_seats(self):
        return self.total_seats

    def __str__(self):
        return f"{self.license_plate}"


#
class BusRoute(models.Model):
    departure_point = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="departure_buses")
    arrival_point = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="arrival_buses")
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_travel_time_in_hours = models.PositiveIntegerField(blank=True, null=True,
                                                                 validators=[MinValueValidator(1)])

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
    departure_date = models.DateField()
    departure_time = models.TimeField()
    arrival_date = models.DateField(blank=True, null=True)
    arrival_time = models.TimeField(blank=True, null=True)
    surcharge = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        if self.bus_route.estimated_travel_time_in_hours:
            departure_datetime = datetime.combine(self.departure_date, self.departure_time)
            travel_time = timedelta(hours=self.bus_route.estimated_travel_time_in_hours)
            self.arrival_date = departure_datetime + travel_time
            self.arrival_time = (departure_datetime + travel_time).time()  #

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bus}:{self.bus_route} Departure: {self.departure_date} {self.arrival_date}"

    class Meta:
        unique_together = (("bus", "departure_date", "departure_time"),)

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    bus_schedule = models.ForeignKey(BusSchedule, on_delete=models.CASCADE, related_name="tickets")
    seat_number = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    booking_status = models.CharField(max_length=20, choices=[('CONFIRMED', 'Confirmed'),
                                                              ('CANCELLED', 'Cancelled')], default='CONFIRMED')

    class Meta:
        unique_together = ['bus_schedule', 'seat_number', 'booking_status']

    def save(self, *args, **kwargs):
        if self.booking_status == 'CONFIRMED':
            existing_confirmed_ticket = Ticket.objects.filter(bus_schedule=self.bus_schedule,
                                                              seat_number=self.seat_number,
                                                              booking_status='CONFIRMED').exists()
            if existing_confirmed_ticket:
                raise ValidationError('This seat is already booked for the selected schedule.')

        bus_schedule = self.bus_schedule
        bus_route = bus_schedule.bus_route
        self.price = bus_route.price + bus_schedule.surcharge
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Ticket #{self.id} - User: {self.user.username}, Seat: {self.seat_number}, Status: {self.booking_status}"
# class CustomerReview(models.Model):
#     reviewed_trip = models.ForeignKey(BusSchedule, on_delete=models.CASCADE,
#                                       related_name="reviews")
#     customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
#     review_text = models.TextField()
#     rating = models.IntegerField(choices=((1, "Poor"), (2, "Fair"), (3, "Good"), (4, "Very Good"), (5, "Excellent")))
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.reviewed_trip}: {self.booking}"
