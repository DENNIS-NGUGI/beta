from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    HousingTarget,
    KenyansOnboarded,
    HousingUnit,
    HousingUnitBought,
)


@admin.register(HousingTarget)
class HousingTargetAdmin(ModelAdmin):
    list_display = ("kpi", "target_value")
    list_filter = ("kpi",)
    search_fields = ("kpi",)


@admin.register(KenyansOnboarded)
class KenyansOnboardedAdmin(ModelAdmin):
    list_display = ("county", "period", "onboarded_count", "target")
    list_filter = ("county", "period")
    search_fields = ("county__name",)


@admin.register(HousingUnit)
class HousingUnitAdmin(ModelAdmin):
    list_display = ("county", "period", "status", "unit_count", "target")
    list_filter = ("county", "period", "status")
    search_fields = ("county__name",)


@admin.register(HousingUnitBought)
class HousingUnitBoughtAdmin(ModelAdmin):
    list_display = ("county", "period", "units_bought")
    list_filter = ("county", "period")
    search_fields = ("county__name",)
