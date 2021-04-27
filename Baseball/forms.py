from django.contrib.contenttypes import forms
from django.forms import ModelForm
from .models import Teams, TeamSelector


class TeamForm(ModelForm):
    class Meta:
        model = Teams
        fields = ['team_id', 'team_name']


class SelectForm(ModelForm):
    class Meta:
        model = TeamSelector
        fields = ['option']
