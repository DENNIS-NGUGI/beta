from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

from .models import (
    County,
    ReportingPeriod,
    ProgrammeTarget,
    FibreLinkDeployment,
    PublicWiFiHotspot,
    ICTDigitalHub,
    DigitalLiteracyStats,
    StudioProduction,
)

@login_required
def dsh(request):
    # Counties for filter
    counties = County.objects.all().order_by("name")
    
    # Reporting years for filter
    years = ReportingPeriod.objects.values_list("year", flat=True).distinct().order_by("year")
    
    # Programme targets
    targets_qs = ProgrammeTarget.objects.all()
    targets = {t.programme: t.target_value for t in targets_qs}

    return render(
        request,
        "pages/dsh/dsh.html",
        {"counties": counties, "years": years, "targets": targets}
    )


# ------------------------------
# Overview for KPI cards
# ------------------------------
@require_GET
def dashboard_overview(request):
    year = request.GET.get("year")
    county_id = request.GET.get("county")

    fibre_qs = FibreLinkDeployment.objects.all()
    literacy_qs = DigitalLiteracyStats.objects.all()
    studio_qs = StudioProduction.objects.all()
    wifi_qs = PublicWiFiHotspot.objects.all()
    ict_qs = ICTDigitalHub.objects.all()

    # ===== Apply year filter =====
    if year:
        fibre_qs = fibre_qs.filter(period__year=year)
        literacy_qs = literacy_qs.filter(period__year=year)
        studio_qs = studio_qs.filter(period__year=year)
        wifi_qs = wifi_qs.filter(installation_date__year=year)  # <--- changed
        ict_qs = ict_qs.filter(period__year=year)

    # ===== Apply county filter =====
    if county_id:
        fibre_qs = fibre_qs.filter(county_id=county_id)
        literacy_qs = literacy_qs.filter(county_id=county_id)
        studio_qs = studio_qs.filter(studio__county_id=county_id)
        wifi_qs = wifi_qs.filter(county_id=county_id)
        ict_qs = ict_qs.filter(county_id=county_id)

    # ===== Return JSON for dashboard KPI cards =====
    return JsonResponse({
        "fibre_km": float(fibre_qs.aggregate(total=Sum("km_added"))["total"] or 0),
        "wifi_hotspots": wifi_qs.count(),
        "ict_hubs": ict_qs.count(),
        "trained_youth": literacy_qs.aggregate(total=Sum("trained"))["total"] or 0,
        "employed_youth": literacy_qs.aggregate(total=Sum("employed"))["total"] or 0,
        "studio_recordings": studio_qs.aggregate(total=Sum("recordings_produced"))["total"] or 0,
    })

# ------------------------------
# Fibre Deployment Analytics
# ------------------------------
@require_GET
def fibre_data(request):
    year = request.GET.get("year")
    county_id = request.GET.get("county")

    qs = FibreLinkDeployment.objects.all()
    if year:
        qs = qs.filter(period__year=year)
    if county_id:
        qs = qs.filter(county_id=county_id)

    trend = qs.values("period__year").annotate(km=Sum("km_added")).order_by("period__year")
    return JsonResponse({"trend": list(trend)})


# ------------------------------
# Public Wi-Fi Analytics
# ------------------------------
@require_GET
def wifi_data(request):
    county_id = request.GET.get("county")
    qs = PublicWiFiHotspot.objects.all()
    if county_id:
        qs = qs.filter(county_id=county_id)

    status_breakdown = qs.values("status").annotate(count=Count("id"))
    return JsonResponse({"by_status": list(status_breakdown)})


# ------------------------------
# Digital Literacy Analytics
# ------------------------------
@require_GET
def digital_literacy_data(request):
    year = request.GET.get("year")
    county_id = request.GET.get("county")

    qs = DigitalLiteracyStats.objects.all()
    if year:
        qs = qs.filter(period__year=year)
    if county_id:
        qs = qs.filter(county_id=county_id)

    totals = qs.aggregate(trained=Sum("trained"), employed=Sum("employed"))
    trained = totals["trained"] or 0
    employed = totals["employed"] or 0

    return JsonResponse({
        "trained": trained,
        "employed": employed,
        "employment_rate": (employed / trained * 100) if trained else 0,
    })


# ------------------------------
# Studio Production Analytics
# ------------------------------
@require_GET
def studio_data(request):
    year = request.GET.get("year")
    county_id = request.GET.get("county")

    qs = StudioProduction.objects.select_related("studio", "studio__county")
    if year:
        qs = qs.filter(period__year=year)
    if county_id:
        qs = qs.filter(studio__county_id=county_id)

    production_by_county = qs.values("studio__county__name").annotate(total_recordings=Sum("recordings_produced")).order_by("-total_recordings")
    production_by_studio = qs.values("studio__name").annotate(total_recordings=Sum("recordings_produced")).order_by("-total_recordings")

    return JsonResponse({
        "by_county": list(production_by_county),
        "by_studio": list(production_by_studio),
    })


# ------------------------------
# ICT Digital Hub Analytics
# ------------------------------
@require_GET
def ict_hub_data(request):
    year = request.GET.get("year")
    county_id = request.GET.get("county")

    qs = ICTDigitalHub.objects.select_related("county")
    if year:
        qs = qs.filter(period__year=year)
    if county_id:
        qs = qs.filter(county_id=county_id)

    by_county = qs.values("county__name", "status").annotate(count=Count("id")).order_by("county__name", "status")
    
    by_status = qs.values("status").annotate(total=Count("id")).order_by("status")

    table_data = {}
    statuses = [s[0] for s in ICTDigitalHub.STATUS_CHOICES]
    for row in by_county:
        county_name = row["county__name"]
        status = row["status"]
        count = row["count"]
        if county_name not in table_data:
            table_data[county_name] = {s: 0 for s in statuses}
        table_data[county_name][status] = count

    county_table = [{"county": k, **v} for k, v in table_data.items()]

    return JsonResponse({
        "by_status": list(by_status),
        "by_county": county_table,
        "statuses": statuses,
    })


