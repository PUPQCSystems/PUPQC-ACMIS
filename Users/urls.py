from django.urls import path
from .views import UserRegistration, BlacklistTokenUpdateView
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistration.as_view(), name="create_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(), name='blacklist'),
    path('', views.landing_page, name='landing'),

]
