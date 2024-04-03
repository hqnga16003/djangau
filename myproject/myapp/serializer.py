from .models import Location
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'



