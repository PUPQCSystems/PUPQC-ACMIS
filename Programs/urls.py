from django.urls import path
from . import views

urlpatterns = [
    path("landing_page/", views.landing_page, name='program-landing'),
]
