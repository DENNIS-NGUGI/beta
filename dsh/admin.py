from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    County,
    ReportingPeriod,
    FibreLinkDeployment,
    PublicWiFiHotspot,
    ICTDigitalHub,
    DigitalLiteracyProgramme,
    DigitalLiteracyStats,
    StudioMashinani,
    StudioProduction,
    MassMediaTraining,
    ProgrammeTarget,
)


@admin.register(County)
class CountyAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

    fieldsets = (
        ("County Information", {
            "fields": ("name",)
        }),
    )


@admin.register(ReportingPeriod)
class ReportingPeriodAdmin(ModelAdmin):
    list_display = ("year", "month")
    list_filter = ("year", "month")
    ordering = ("year", "month")

    fieldsets = (
        ("Reporting Period", {
            "fields": ("year", "month")
        }),
    )


@admin.register(FibreLinkDeployment)
class FibreLinkDeploymentAdmin(ModelAdmin):
    list_display = ("link_name", "county", "period", "km_added", "created_at")
    search_fields = ("link_name", "county__name")
    list_filter = ("county", "period")
    ordering = ("period__year", "period__month")
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Deployment Details", {
            "fields": ("link_name", "county", "period", "km_added")
        }),
        ("Metadata", {
            "fields": ("created_at",)
        }),
    )


@admin.register(PublicWiFiHotspot)
class PublicWiFiHotspotAdmin(ModelAdmin):
    list_display = ("location", "county", "status", "installation_date")
    search_fields = ("location", "county__name")
    list_filter = ("county", "status")
    ordering = ("county", "location")

    fieldsets = (
        ("Hotspot Details", {
            "fields": ("location", "county", "status", "installation_date")
        }),
    )


@admin.register(ICTDigitalHub)
class ICTDigitalHubAdmin(ModelAdmin):
    list_display = ("location", "county", "status", "completion_date", "period")
    search_fields = ("location", "county__name")
    list_filter = ("county", "status", "period")
    ordering = ("county", "period")

    fieldsets = (
        ("Hub Details", {
            "fields": ("location", "county", "status", "completion_date", "period")
        }),
    )


@admin.register(DigitalLiteracyProgramme)
class DigitalLiteracyProgrammeAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

    fieldsets = (
        ("Programme Information", {
            "fields": ("name",)
        }),
    )


@admin.register(DigitalLiteracyStats)
class DigitalLiteracyStatsAdmin(ModelAdmin):
    list_display = ("programme", "county", "period", "trained", "employed")
    list_filter = ("programme", "county", "period")
    search_fields = ("programme__name", "county__name")
    ordering = ("period", "county")

    fieldsets = (
        ("Digital Literacy Stats", {
            "fields": ("programme", "county", "period", "trained", "employed")
        }),
    )


@admin.register(StudioMashinani)
class StudioMashinaniAdmin(ModelAdmin):
    list_display = ("name", "county", "location", "status", "period")
    search_fields = ("name", "location", "county__name")
    list_filter = ("county", "status", "period")
    ordering = ("county", "name")

    fieldsets = (
        ("Studio Details", {
            "fields": ("name", "county", "location", "status", "period")
        }),
    )


@admin.register(StudioProduction)
class StudioProductionAdmin(ModelAdmin):
    list_display = ("studio", "period", "recordings_produced")
    search_fields = ("studio__name", "studio__county__name")
    list_filter = ("studio__county", "period")
    ordering = ("period",)

    fieldsets = (
        ("Studio Production", {
            "fields": ("studio", "period", "recordings_produced")
        }),
    )


@admin.register(MassMediaTraining)
class MassMediaTrainingAdmin(ModelAdmin):
    list_display = ("county", "period", "students_trained")
    list_filter = ("county", "period")
    ordering = ("period", "county")
    search_fields = ("county__name",)

    fieldsets = (
        ("Training Details", {
            "fields": ("county", "period", "students_trained")
        }),
    )


@admin.register(ProgrammeTarget)
class ProgrammeTargetAdmin(ModelAdmin):
    list_display = ("programme", "target_value", "start_year", "end_year")
    search_fields = ("programme",)
    ordering = ("programme", "start_year")

    fieldsets = (
        ("Target Details", {
            "fields": ("programme", "target_value", "start_year", "end_year")
        }),
    )
