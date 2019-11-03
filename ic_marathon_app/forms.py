from django import forms
from django_select2.forms import Select2Widget
from .models import Team,Workout


class UserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.team = forms.ChoiceField(

            widget=Select2Widget(
                queryset=Team.objects.all().order_by('team_name'),
                search_fields=['team_name__icontains']
            ),
            queryset=Team.objects.all().order_by('team_name'),
            label='Team:',
            required=True)



