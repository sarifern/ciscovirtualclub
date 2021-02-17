from django.contrib import admin
from .models import Workout, Profile
from django.utils.html import format_html
# Register your models here.


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'belongs_to', 'distance')
    list_filter = ['belongs_to']



admin.site.register(Workout, WorkoutAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email','has_donated', 'distance')
    list_filter = ['user', 'email']


admin.site.register(Profile, ProfileAdmin)
