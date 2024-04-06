from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status,parsers
from rest_framework.response import Response

from .models import Location
from .serializer import LocationSerializer
# from .paginator import CoursePaginator
from rest_framework.decorators import action
from .perms import OwnerPermission

from rest_framework.permissions import IsAuthenticated

class LocationViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]





