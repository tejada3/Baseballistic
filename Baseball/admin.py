from django.contrib import admin
from .models import *


@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ['team_id', 'team_name']