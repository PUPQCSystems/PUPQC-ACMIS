from django.urls import path
# from .views import UserRegistration
from . import views

app_name = 'index'

urlpatterns = [
    # path('', views.index_page, name='index-page'),
    path('about/', views.about_page, name='about-page'),
    path('', views.login_page, name='login-page'),


]
