from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status, parsers
from rest_framework.response import Response

from .models import Location, User
from .serializer import LocationSerializer, UserSerializer
# from .paginator import CoursePaginator
from rest_framework.decorators import action
from .perms import OwnerPermission


class LocationViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('get_current'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current", detail=False)
    def get_current(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

