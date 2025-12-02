from django.shortcuts import render
from .models import County, HealthRecord
from django.db.models import F, FloatField, ExpressionWrapper, Sum

def dashboard(request):
    return render(request, 'pages/index.html')

def agriculture(request):
    return render(request, 'pages/agriculture.html')

def about(request):
    return render(request, 'pages/about.html')

def msme(request):
    return render(request, 'pages/msme.html')

def pillars(request):
    return render(request, 'pages/pillars.html')

def projects(request):
    return render(request, 'pages/projects.html')

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
    
    monthly_totals = (
        HealthRecord.objects
        .values("month_and_year")
        .annotate(
            total_diabetes=Sum("diabetes_cases"),
            total_hypertension=Sum("hypertension_cases"),
        )
        .order_by("month_and_year")
    )

    chart_labels = [entry["month_and_year"] for entry in monthly_totals]
    diabetes_data = [entry["total_diabetes"] for entry in monthly_totals]
    hypertension_data = [entry["total_hypertension"] for entry in monthly_totals]

    return render(request, "pages/uhc.html", {
        "counties": leaflet_data,
        "total_sha": total_sha,
        "total_percentage": total_percentage,
        "total_population": total_population,
        "chart_labels": chart_labels,
        "diabetes_data": diabetes_data,
        "hypertension_data": hypertension_data,
    })

def housing(request):
    return render(request, 'pages/housing.html')

def digital(request):
    return render(request, 'pages/digital.html')

def login(request):
    return render(request, 'bauth/login.html')