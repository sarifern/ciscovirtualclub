from django.contrib import admin
from .models import Workout, Profile
# Register your models here.


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'belongs_to', 'distance', "photo_evidence")
    list_filter = ['belongs_to']


admin.site.register(Workout, WorkoutAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cec', 'user_goal', 'distance')
    list_filter = ['user', 'cec']


admin.site.register(Profile, ProfileAdmin)
