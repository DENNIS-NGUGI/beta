from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

from .models import (
    County,
    ReportingPeriod,
    HousingTarget,
    KenyansOnboarded,
    HousingUnit,
    HousingUnitBought,
)


@login_required
def housing_dashboard(request):
    counties = County.objects.all().order_by("name")
    years = ReportingPeriod.objects.values_list("year", flat=True).distinct().order_by("year")

    targets = {
        'kenyans_onboarded': HousingTarget.objects.get(kpi='kenyans_onboarded').target_value,
        'units_completed': HousingTarget.objects.get(kpi='units').target_value,
        'units_bought': HousingTarget.objects.get(kpi='units').target_value,
        'units_pending': 'N/A'
    }
 
    return render(
        request,
        "pages/housing/housing_dashboard.html",
        {"counties": counties, "years": years, "targets": targets}
    )


@require_GET
def housing_overview(request):
    year = request.GET.get("year")
    county_id = request.GET.get("county")

    onboarded_qs = KenyansOnboarded.objects.all()
    units_qs = HousingUnit.objects.all()
    bought_qs = HousingUnitBought.objects.all()

    # Apply filters
    if year:
        onboarded_qs = onboarded_qs.filter(period__year=year)
        units_qs = units_qs.filter(period__year=year)
        bought_qs = bought_qs.filter(period__year=year)
    if county_id:
        onboarded_qs = onboarded_qs.filter(county_id=county_id)
        units_qs = units_qs.filter(county_id=county_id)
        bought_qs = bought_qs.filter(county_id=county_id)

    completed_units = units_qs.filter(status="completed").aggregate(total=Sum("unit_count"))["total"] or 0
    pending_units = units_qs.filter(status="pending").aggregate(total=Sum("unit_count"))["total"] or 0

    return JsonResponse({
        "kenyans_onboarded": onboarded_qs.aggregate(total=Sum("onboarded_count"))["total"] or 0,
        "units_completed": completed_units,
        "units_pending": pending_units,
        "units_bought": bought_qs.aggregate(total=Sum("units_bought"))["total"] or 0,
    })


# ------------------------------
# Kenyans Onboarded Analytics
# ------------------------------
@require_GET
def kenyans_onboarded_data(request):
    year = request.GET.get("year")
    county_id = request.GET.get("county")

    qs = KenyansOnboarded.objects.select_related("county")
    if year:
        qs = qs.filter(period__year=year)
    if county_id:
        qs = qs.filter(county_id=county_id)

    table_data = qs.values("county__name").annotate(total_onboarded=Sum("onboarded_count")).order_by("county__name")
    return JsonResponse({"by_county": list(table_data)})


# ------------------------------
# Housing Units Analytics
# ------------------------------
@require_GET
def units_data(request):
    year = request.GET.get("year")
    county_id = request.GET.get("county")

    qs = HousingUnit.objects.select_related("county")
    if year:
        qs = qs.filter(period__year=year)
    if county_id:
        qs = qs.filter(county_id=county_id)

    # Aggregate completed and pending separately
    completed = qs.filter(status="completed").values("county__name").annotate(total=Sum("unit_count")).order_by("county__name")
    pending = qs.filter(status="pending").values("county__name").annotate(total=Sum("unit_count")).order_by("county__name")

    return JsonResponse({"completed": list(completed), "pending": list(pending)})


# ------------------------------
# Units Bought Analytics
# ------------------------------
@require_GET
def units_bought_data(request):
    year = request.GET.get("year")
    county_id = request.GET.get("county")

    qs = HousingUnitBought.objects.select_related("county")
    if year:
        qs = qs.filter(period__year=year)
    if county_id:
        qs = qs.filter(county_id=county_id)

    table_data = qs.values("county__name").annotate(total_bought=Sum("units_bought")).order_by("county__name")
    return JsonResponse({"by_county": list(table_data)})
