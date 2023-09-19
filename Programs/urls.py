from django.urls import path
from . import views

urlpatterns = [
    path("landing_page/", views.landing_page, name='program-landing'),
    path("program_create/", views.create_program, name='program-create'),
    path("program_update/<str:pk>/", views.update_program, name='program-update'),
]
