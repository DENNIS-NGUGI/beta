from  django.urls import path
from . import views

urlpatterns = [
    path('', views.bi_index, name='bi_index'),
    path('agriculture/', views.bi_agriculture, name='bi_agriculture'),
    path('digital/', views.bi_digital, name='bi_digital'),
    path('housing/', views.bi_housing, name='bi_housing'),
    path('msme/', views.bi_msme, name='bi_msme'),
    path('uhc/', views.bi_uhc, name='bi_uhc')
]
