from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    UHCTarget,
    SHAOnboarded,
    SHAIndividualsTreated,
    SHADisbursement,
    HealthFacilityDigitized,
)


@admin.register(UHCTarget)
class UHCTargetAdmin(ModelAdmin):
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


@admin.register(SHAOnboarded)
class SHAOnboardedAdmin(ModelAdmin):
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
        ("SHA Onboarding Data", {
            "fields": ("county", "period", "onboarded_count")
        }),
        ("Target Mapping", {
            "fields": ("target",)
        }),
    )

    @admin.display(description="Coverage (%)")
    def percentage_covered_display(self, obj):
        return f"{obj.percentage_covered():.2f}%"


@admin.register(SHAIndividualsTreated)
class SHAIndividualsTreatedAdmin(ModelAdmin):
    list_display = (
        "county",
        "period",
        "treated_count",
        "target",
        "percentage_covered_display",
    )
    list_filter = ("county", "period")
    search_fields = ("county__name",)
    ordering = ("period", "county")

    fieldsets = (
        ("Treatment Data", {
            "fields": ("county", "period", "treated_count")
        }),
        ("Target Mapping", {
            "fields": ("target",)
        }),
    )

    @admin.display(description="Coverage (%)")
    def percentage_covered_display(self, obj):
        return f"{obj.percentage_covered():.2f}%"


@admin.register(SHADisbursement)
class SHADisbursementAdmin(ModelAdmin):
    list_display = (
        "county",
        "period",
        "amount_disbursed",
        "target",
        "percentage_covered_display",
    )
    list_filter = ("county", "period")
    search_fields = ("county__name",)
    ordering = ("period", "county")

    fieldsets = (
        ("Disbursement Data", {
            "fields": ("county", "period", "amount_disbursed")
        }),
        ("Target Mapping", {
            "fields": ("target",)
        }),
    )

    @admin.display(description="Coverage (%)")
    def percentage_covered_display(self, obj):
        return f"{obj.percentage_covered():.2f}%"


@admin.register(HealthFacilityDigitized)
class HealthFacilityDigitizedAdmin(ModelAdmin):
    list_display = (
        "county",
        "period",
        "digitized_count",
        "target",
        "percentage_covered_display",
    )
    list_filter = ("county", "period")
    search_fields = ("county__name",)
    ordering = ("period", "county")

    fieldsets = (
        ("Digitization Data", {
            "fields": ("county", "period", "digitized_count")
        }),
        ("Target Mapping", {
            "fields": ("target",)
        }),
    )

    @admin.display(description="Coverage (%)")
    def percentage_covered_display(self, obj):
        return f"{obj.percentage_covered():.2f}%"
