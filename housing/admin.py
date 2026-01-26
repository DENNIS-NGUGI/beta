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
    list_display = ("kpi", "county", "target_value", "start_year", "end_year")
    list_filter = ("kpi", "county", "start_year", "end_year")
    search_fields = ("kpi", "county__name")
    ordering = ("kpi", "county", "start_year")

    fieldsets = (
        ("Target Definition", {
            "fields": ("kpi", "county")
        }),
        ("Target Period", {
            "fields": ("target_value", "start_year", "end_year")
        }),
    )


@admin.register(KenyansOnboarded)
class KenyansOnboardedAdmin(ModelAdmin):
    list_display = (
        "county",
        "period",
        "onboarded_count",
        "target",
        "percentage_covered_display",
    )
    list_filter = ("county", "period")
    search_fields = ("county__name",)
    ordering = ("period", "county")

    fieldsets = (
        ("Onboarding Data", {
            "fields": ("county", "period", "onboarded_count")
        }),
        ("Target Mapping", {
            "fields": ("target",)
        }),
    )

    @admin.display(description="Coverage (%)")
    def percentage_covered_display(self, obj):
        return f"{obj.percentage_covered():.2f}%"


@admin.register(HousingUnit)
class HousingUnitAdmin(ModelAdmin):
    list_display = (
        "county",
        "period",
        "status",
        "unit_count",
        "target",
        "percentage_covered_display",
    )
    list_filter = ("county", "period", "status")
    search_fields = ("county__name",)
    ordering = ("period", "county", "status")

    fieldsets = (
        ("Housing Unit Details", {
            "fields": ("county", "period", "status", "unit_count")
        }),
        ("Target Mapping", {
            "fields": ("target",)
        }),
    )

    @admin.display(description="Coverage (%)")
    def percentage_covered_display(self, obj):
        return f"{obj.percentage_covered():.2f}%"


@admin.register(HousingUnitBought)
class HousingUnitBoughtAdmin(ModelAdmin):
    list_display = (
        "county",
        "period",
        "units_bought",
        "target",
        "percentage_covered_display",
    )
    list_filter = ("county", "period")
    search_fields = ("county__name",)
    ordering = ("period", "county")

    fieldsets = (
        ("Units Bought Data", {
            "fields": ("county", "period", "units_bought")
        }),
        ("Target Mapping", {
            "fields": ("target",)
        }),
    )

    @admin.display(description="Coverage (%)")
    def percentage_covered_display(self, obj):
        return f"{obj.percentage_covered():.2f}%"
