from django.urls import path

from Users import views_activities
# from .views import UserRegistration
from . import views, views_profile

app_name = 'users'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('register/', views.register_account, name="create_user"),
    path('update/<str:pk>/', views.update_account, name="update-account"),
    path('deactivate/<str:pk>/', views.deactivate_account, name="deactivate-user"),

    path('archive_page/', views.archive_landing, name="archive-landing"),
    path('archive_page/restore/<str:pk>/', views.reactivate_account, name="restore-user"),

    path('profile/<str:pk>/', views.deactivate_account, name="profile-user"),
    path('profile/', views_profile.landing_page, name="profile"),

    path('activities/', views_activities.admin_activities, name="admin-activity-log"),

    path('activities/', views_activities.user_activities, name="user-activity-log"),



]
