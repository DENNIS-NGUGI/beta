"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('db2duKpzJrZUaUxlODHnXpMEEJ_5cs7rtK4gb9L_0LI/', admin.site.urls),
    path('', include('betadash.urls')),
    path('beta/auth/', include('beta_auth.urls')),
    path('dsh/', include('dsh.urls')),
    path('uhc/', include('uhc.urls')),
    path('housing/', include('housing.urls')),
    path('agriculture/', include('agriculture.urls')),
    path('msme/', include('msme.urls')),
    path('bi/', include('bi.urls'))
]
