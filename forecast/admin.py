# admin.py
from django.contrib import admin
from .models import Reservoir


@admin.register(Reservoir)
class ResorvoirDataAdmin(admin.ModelAdmin):
    list_display = (
        'reservoir_name', 'basin', 
        'year', 'month', 'full_reservoir_level', 'live_capacity_frl', 
        'storage', 'level'
    )