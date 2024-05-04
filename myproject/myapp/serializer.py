from .models import Location, User, Bus, BusRoute, BusSchedule, Ticket
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'user_type']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def get_avatar(self, obj):
        if obj.user.avatar:
            return obj.user.avatar.url
        return None


class BusSerializer(ModelSerializer):
    class Meta:
        model = Bus
        fields = ['id', 'license_plate', 'total_seats']


class BusRouteSerializer(ModelSerializer):
    class Meta:
        model = BusRoute
        fields = ['id', 'departure_point', 'arrival_point', 'is_active', 'price', 'estimated_travel_time_in_hours']


class BusScheduleSerializer(ModelSerializer):
    class Meta:
        model = BusSchedule
        fields = '__all__'

class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
