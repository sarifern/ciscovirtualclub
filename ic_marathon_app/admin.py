from django.contrib import admin
from .models import Workout
# Register your models here.
class WorkoutAdmin(admin.ModelAdmin):
    list_display=('uuid',)
    list_filter = ['uuid']

admin.site.register(Workout,WorkoutAdmin)