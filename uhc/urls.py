from django.urls import path
from . import views

urlpatterns = [
    path("", views.uhc_dashboard, name="uhc"),
    # path("api/overview/", views.uhc_overview, name="overview"),
    # path("api/onboarded/", views.onboarded_data, name="onboarded-data"),
    # path("api/treated/", views.treated_data, name="treated-data"),
    # path("api/disbursement/", views.disbursement_data, name="disbursement-data"),
    # path("api/digitized-facilities/", views.digitized_facilities_data, name="digitized-data"),
]
