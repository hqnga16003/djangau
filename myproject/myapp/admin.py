from django import forms
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import mark_safe
from .models import Category
from django.contrib.auth.models import Permission
from ckeditor_uploader.widgets import CKEditorUploadingWidget


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

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['id', 'name']
    search_fields = ['name']



admin_site = AppAdminSite(name="myapp")

admin_site.register(Category,CategoryAdmin)
admin_site.register(Permission)
