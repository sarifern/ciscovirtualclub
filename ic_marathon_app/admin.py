from django.contrib import admin
from .models import Workout, Team, Profile
# Register your models here.


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'belongs_to')
    list_filter = ['uuid']


admin.site.register(Workout, WorkoutAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'team_distance')
    list_filter = ['team_name']


admin.site.register(Team,TeamAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','cec', 'distance','team')
    list_filter = ['user','cec','team']


admin.site.register(Profile,ProfileAdmin)
