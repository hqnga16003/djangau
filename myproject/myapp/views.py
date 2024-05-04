from datetime import date

from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status, parsers, filters
from rest_framework.response import Response

from .models import Location, User, Bus, BusRoute, BusSchedule, Ticket
from .serializer import LocationSerializer, UserSerializer, BusSerializer, BusRouteSerializer, BusScheduleSerializer, \
    TicketSerializer
# from .paginator import CoursePaginator
from rest_framework.decorators import action
from .perms import OwnerPermission

from rest_framework.permissions import IsAuthenticated


class LocationViewSet(viewsets.ViewSet, generics.ListCreateAPIView, ):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = 'id'

    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        locations = self.get_queryset()
        serializer = self.serializer_class(locations, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

        if ticket.user != request.user:
            return Response({"error": "You don't have permission to update this ticket"},
                            status=status.HTTP_403_FORBIDDEN)

        ticket.booking_status = 'CANCELLED'
        ticket.save()

        serializer = TicketSerializer(ticket)
        return Response(serializer.data)
class UserViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action.__eq__('get_current'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current", detail=False)
    def get_current(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

    @action(methods=['put'], url_path="update", detail=False)
    def update_current_user(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    # permission_classes = [permissions.IsAuthenticated]


class BusRouteViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        id_departure_point = request.query_params.get('id_departure_point')
        id_arrival_point = request.query_params.get('id_arrival_point')

        if not id_departure_point:
            return Response({'error': 'Vui lòng cung cấp id_departure_point'}, status=400)
        if not id_arrival_point:
            return Response({'error': 'Vui lòng cung cấp id_arrival_point'}, status=400)
        bus_routes = BusRoute.objects.filter(departure_point_id=id_departure_point, arrival_point_id=id_arrival_point,
                                             is_active=True)
        serializer = self.serializer_class(bus_routes, many=True)
        return Response(serializer.data)


class BusScheduleViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = BusSchedule.objects.all()
    serializer_class = BusScheduleSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        departure_point = request.query_params.get('id_departure_point')
        arrival_point = request.query_params.get('id_arrival_point')
        departure_date = request.query_params.get('departure_date')

        if not departure_point:
            return Response({'error': 'Missing location_id parameter'}, status=400)
        if not arrival_point:
            return Response({'error': 'Missing location_id parameter'}, status=400)
        if not departure_date:
            return Response({'error': 'Missing departure_date parameter'}, status=400)

        try:
            id_departure_point = int(departure_point)
            id_arrival_point = int(arrival_point)
            departure_date_obj = date.fromisoformat(departure_date)

        except ValueError:
            return Response({'error': 'Invalid location_id format (must be an integer)'}, status=400)

        queryset = BusSchedule.objects.filter(bus_route__departure_point=id_departure_point,
                                              bus_route__arrival_point=id_arrival_point,departure_date=departure_date_obj)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class TicketViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Ticket.objects.all()  # Get all tickets by default
    serializer_class = TicketSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['booking_date']
    permission_classes = [permissions.IsAuthenticated]

    filter_backends.append(filters.OrderingFilter)
    filterset_fields = ['booking_status']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        booking_status = self.request.query_params.get('booking_status')
        queryset = queryset.filter(user=user)
        if booking_status:
            queryset = queryset.filter(booking_status=booking_status)
        return queryset

    def create(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = TicketSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

        if ticket.user != request.user:
            return Response({"error": "You don't have permission to update this ticket"},
                            status=status.HTTP_403_FORBIDDEN)

        ticket.booking_status = 'CANCELLED'
        ticket.save()

        serializer = TicketSerializer(ticket)
        return Response(serializer.data)