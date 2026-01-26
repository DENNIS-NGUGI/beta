from django.urls import path
from . import views

urlpatterns = [
    path('', views.dsh, name='dsh'),
    path('api/dashboard-overview/', views.dashboard_overview, name='dashboard_overview'),
    path('api/fibre/', views.fibre_data, name='fibre_data'),
    path('api/wifi/', views.wifi_data, name='wifi_data'),
    path('api/literacy/', views.digital_literacy_data, name='digital_literacy_data'),
    path('api/studio-production/', views.studio_data, name='studio_data'),
    path('api/ict-hub/', views.ict_hub_data, name='ict_hub_data'), 
]
