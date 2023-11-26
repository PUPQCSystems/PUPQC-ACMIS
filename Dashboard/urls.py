from django.urls import path
from . import views

app_name = 'dashboards'

urlpatterns = [
    path("", views.landing_page, name='dashboard-landing'),
]
