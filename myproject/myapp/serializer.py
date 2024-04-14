from .models import Location, User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class BaseSerializer(ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            if request:
                return request.build_absolute_uri("/static/%s" % obj.image.name)
            return "/%s" % obj.image.name


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar']



