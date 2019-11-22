import django_tables2 as tables
from django.utils.html import format_html
from .models import Workout, Profile


class ProfileTable(tables.Table):
    def render_avatar(self, value):
        return format_html('<img src="{}" height="42" width="42"/>', value)

    class Meta:
        model = Profile
        attrs = {"class": "table "}
        fields = ("avatar", "cec", "distance")
        row_attrs = {
            'user-goal': lambda record: record.user_goal
        }


class WorkoutTable(tables.Table):
    def render_time(self, value):
        return format_html("{} min.", value.hour*60+value.minute)

    def render_distance(self, value):
        return format_html("{} K", value)

    def render_photo_evidence(self, value):
        return format_html('<img src="{}" height="42" width="42"/>', value.url)

    class Meta:
        model = Workout

        attrs = {"class": "table table--striped"}
        fields = ("distance", "time", "photo_evidence")
