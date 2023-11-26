"""
URL configuration for ACIS_system_v1 project.

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
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),

    path('programs/', include('Programs.urls', namespace='programs')), 
    path('dashboard/', include('Dashboard.urls', namespace='dashboards')),
    path('accreditation/', include('Accreditation.urls', namespace= 'accreditation')),
    path('user/', include('Users.urls', namespace ='users')),

    path('', include('LandingPage.urls', namespace = 'index')),

    path('accounts/', include('django.contrib.auth.urls')),

]

