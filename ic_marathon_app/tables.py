import django_tables2 as tables
from django_tables2 import TemplateColumn
from django.utils.html import format_html
from .models import Workout, Profile
from badgify.models import Award
from django.contrib.auth.models import User


class ProfileTable(tables.Table):
    awards = tables.Column(empty_values=())

    def render_awards(self, value,record):
        awards_html = ""
        earned_awards = Award.objects.filter(user=record.user)
        for award in earned_awards:
            awards_html += '<img src="{}" height="42" width="42"/>'.format(award.badge.image.url)
        return format_html(awards_html)

    def render_avatar(self, value):
        return format_html('<img src="{}" height="42" width="42"/>', value)

    class Meta:
        model = Profile
        attrs = {"class": "table "}
        fields = ("avatar", "cec", "distance","awards")
        row_attrs = {
            'user-goal': lambda record: record.user_goal
        }


class WorkoutTable(tables.Table):
    delete = TemplateColumn(
        template_name='tables/workout_delete_column.html')

    def render_time(self, value):
        return format_html("{} min.", value.hour*60+value.minute)

    def render_distance(self, value):
        return format_html("{} K", value)

    def render_photo_evidence(self, value):
        return format_html('<img src="{}" height="42" width="42"/>', value.url)

    class Meta:
        model = Workout

        attrs = {"class": "table table--striped"}
        fields = ("distance", "time", "photo_evidence", "delete")
