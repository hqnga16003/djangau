from django import forms
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import mark_safe
from django.contrib.auth.models import Permission
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from myapp.models import Location, User, Bus, BusRoute, BusSchedule, Ticket


class AppAdminSite(admin.AdminSite):
    site_header = "Nam Dau Khac"

    # def get_urls(self):
    #     return [
    #                path('course-stats/', self.stats_view)
    #            ] + super().get_urls()
    #
    # def stats_view(self, request):
    #     stats = count_course_by_cate()
    #     return TemplateResponse(request, 'admin/stats_view.html',{
    #         'stats': stats
    #     })


class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'avatar', 'user_type']


class BusAdmin(admin.ModelAdmin):
    list_display = ['id', 'license_plate', 'total_seats']


class BusRouteAdmin(admin.ModelAdmin):
    list_display = ['id', 'departure_point', 'arrival_point', 'is_active', 'price', 'estimated_travel_time_in_hours']


class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'bus', 'bus_route', 'departure_date', 'departure_time', 'arrival_date', 'arrival_time',
                    'surcharge']


class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bus_schedule', 'seat_number', 'booking_date', 'booking_status', ]


#
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ['id', 'bus_schedule', 'sales_staff','customer', 'is_active', 'created_at', 'total_seats']
#
#
# class SeatAdmin(admin.ModelAdmin):
#     list_display = ['id', 'number_seat', 'booking']
#
#
# class CustomerReviewAdmin(admin.ModelAdmin):
#     list_display = ['id', 'reviewed_trip', 'customer', 'review_text', 'rating', 'created_at']


admin_site = AppAdminSite(name="myapp")

admin_site.register(User, UserAdmin)
admin_site.register(Location, LocationAdmin)
admin_site.register(Bus, BusAdmin)
admin_site.register(BusRoute, BusRouteAdmin)

admin_site.register(BusSchedule, BusScheduleAdmin)
admin_site.register(Ticket, TicketAdmin)

# admin_site.register(Bus, BusAdmin)
# admin_site.register(BusSchedule, BusScheduleAdmin)
# admin_site.register(Booking, BookingAdmin)
# admin_site.register(Seat, SeatAdmin)
# admin_site.register(CustomerReview, CustomerReviewAdmin)

admin_site.register(Permission)
