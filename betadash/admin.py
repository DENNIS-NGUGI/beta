from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import County, HealthRecord, DSH

@admin.register(County)
class CountyAdmin(ModelAdmin):
    list_display = ('name', 'sha_registrations', 'population', 'latitude', 'longitude')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    list_per_page = 50

    unfold_fields = {
        'County Information': ('name',),
        'Statistics': ('sha_registrations', 'population'),
        'Location': ('latitude', 'longitude'),
    }
    
@admin.register(HealthRecord)
class HealthRecordAdmin(ModelAdmin):
    list_display = ('county', 'month_and_year', 'diabetes_cases', 'hypertension_cases')
    search_fields = ('county',)
    list_filter = ('county', 'month_and_year')
    ordering = ('county', 'month_and_year')
    list_per_page = 50

    unfold_fields = {
        'County & Date': ('county', 'month_and_year'),
        'Health Statistics': ('diabetes_cases', 'hypertension_cases'),
    }

@admin.register(DSH)
class DSHAdmin(ModelAdmin):
    pass