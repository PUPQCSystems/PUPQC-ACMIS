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
from Dashboard import views as dashboard_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("programs/", include("Programs.urls")), 

    path("dashboard/", include("Dashboard.urls")),
    path("accreditation/", include("Accreditation.urls")),

    path('', dashboard_views.index_page, name='index-page'),

    path("api/user/", include("Users.urls", namespace ='users')),
    path('api-auth/', include('rest_framework.urls', namespace ='rest_framework')),

]

