from django.urls import path
from . import views

app_name = 'dashboards'

urlpatterns = [
    path("", views.landing_page, name='dashboard-landing'),
    path("load-folders/<str:pk>/<str:record_id>/", views.folder_view, name='load-folders'),
]
