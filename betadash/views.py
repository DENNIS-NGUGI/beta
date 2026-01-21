from django.shortcuts import render
from .models import County, HealthRecord, DSH
from django.db.models import F, FloatField, ExpressionWrapper, Sum
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'pages/index.html')

@login_required
def agriculture(request):
    return render(request, 'pages/agriculture.html')

@login_required
def about(request):
    return render(request, 'pages/about.html')

@login_required
def msme(request):
    return render(request, 'pages/msme.html')

@login_required
def pillars(request):
    return render(request, 'pages/pillars.html')

@login_required
def projects(request):
    return render(request, 'pages/projects.html')

@login_required
def uhc(request):
    counties = County.objects.annotate(
        sha_percentage=ExpressionWrapper(
            F('sha_registrations') * 100.0 / F('population'),
            output_field=FloatField()
        )
    )
    leaflet_data = [
        {
            "name": county.name,
            "latitude": float(county.latitude),
            "longitude": float(county.longitude),
            "sha_registrations": county.sha_registrations,
            "population": county.population,
            "sha_percentage": round(county.sha_percentage, 2)
        }
        for county in counties
    ]
    totals = County.objects.aggregate(
    total_sha=Sum('sha_registrations'),
    total_population=Sum('population')
    )
    total_sha = totals['total_sha'] or 0
    total_population = totals['total_population'] or 1
    total_percentage = round(total_sha * 100.0 / total_population, 2)
    
    raw_monthly  = (
        HealthRecord.objects
        .values("month_and_year")
        .annotate(
            total_diabetes=Sum("diabetes_cases"),
            total_hypertension=Sum("hypertension_cases"),
        )
    )
    raw_monthly = list(raw_monthly)
    def parse_month_year(text):
        return datetime.strptime(text, "%B %Y")
    raw_monthly.sort(key=lambda x: parse_month_year(x["month_and_year"]))
    chart_labels = [entry["month_and_year"] for entry in raw_monthly]
    diabetes_data = [entry["total_diabetes"] for entry in raw_monthly]
    hypertension_data = [entry["total_hypertension"] for entry in raw_monthly]

    return render(request, "pages/uhc.html", {
        "counties": leaflet_data,
        "total_sha": total_sha,
        "total_percentage": total_percentage,
        "total_population": total_population,
        "chart_labels": chart_labels,
        "diabetes_data": diabetes_data,
        "hypertension_data": hypertension_data,
        "diabetes_total": sum(diabetes_data),
        "hypertension_total": sum(hypertension_data)
    })

@login_required
def housing(request):
    return render(request, 'pages/housing.html')

@login_required
def digital(request):
    links = DSH.objects.all()

    for link in links:
        link.overall_scope_km = round(link.overall_scope_m / 1000, 2)
        link.open_trench_km = round(link.open_trench_m / 1000, 2)
        link.backfilled_km = round(link.backfilled_m / 1000, 2)
        link.fibre_blown_km = round(link.fibre_blown_m / 1000, 2)
    
    total_open_trench_m = links.aggregate(Sum('open_trench_m'))['open_trench_m__sum'] or 0
    total_backfilled_m = links.aggregate(Sum('backfilled_m'))['backfilled_m__sum'] or 0
    total_fibre_blown_m = links.aggregate(Sum('fibre_blown_m'))['fibre_blown_m__sum'] or 0
    
    total_open_trench_km = round(total_open_trench_m / 1000, 2)
    total_backfilled_km = round(total_backfilled_m / 1000, 2)
    total_fibre_blown_km = round(total_fibre_blown_m / 1000, 2)

    total_fibre_connectivity_km = round(links.aggregate(Sum('overall_scope_m'))['overall_scope_m__sum'] / 1000, 2) if links.exists() else 0

    context = {
        'links': links,
        'total_fibre_connectivity_km': total_fibre_connectivity_km,
        'total_open_trench_km': total_open_trench_km,
        'total_backfilled_km': total_backfilled_km,
        'total_fibre_blown_km': total_fibre_blown_km,
    }
    return render(request, 'pages/digital.html', context)