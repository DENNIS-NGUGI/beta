from django.urls import path
from . import views

urlpatterns = [
    path("", views.housing_dashboard, name="housing"),
    path("api/overview/", views.housing_overview, name="housing-overview"),
    path("api/onboarded/", views.kenyans_onboarded_data, name="housing-onboarded-data"),
    path("api/units/", views.units_data, name="housing-units-data"),
    path("api/units-bought/", views.units_bought_data, name="housing-units-bought-data"),
]
