from django.contrib import admin
from .models import Workout, Profile
# Register your models here.


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'belongs_to', 'distance')
    list_filter = ['uuid']


admin.site.register(Workout, WorkoutAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cec', 'user_goal', 'distance')
    list_filter = ['user', 'cec']


admin.site.register(Profile, ProfileAdmin)

