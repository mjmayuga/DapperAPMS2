"""
URL configuration for dapperAPMS project. happylang

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import views
from .views import PatientDataListAPIView

urlpatterns = [
    path("", views.indexpage, name = 'index'),
    path("AllPatients/", views.AllPatientspage, name = 'allpatients'),
    path("Collaborators/", views.Collaboratorspage, name = 'collaborators'),
    path("Dashboard/", views.Dashboardpage, name = 'dashboard'),
    path("login/", views.loginpage, name = 'login'),
    path("OnGoing/", views.OnGoingpage, name = 'ongoing'),
    path("SettingAlarm/", views.SettingAlarmpage, name = 'settingalarm'),
    path("Settings/", views.Settingspage, name = 'settings'),
    path('admin/', admin.site.urls)
]
