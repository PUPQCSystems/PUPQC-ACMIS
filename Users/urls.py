from django.urls import path
from .views import UserRegistration
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistration.as_view(), name="create_user"),
    path('', views.landing_page, name='landing'),

]
