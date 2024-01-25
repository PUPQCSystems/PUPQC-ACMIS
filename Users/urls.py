from django.urls import path

from Users import views_activities, views_user_groups
# from .views import UserRegistration
from . import views_profile, views_user


app_name = 'users'

urlpatterns = [
    path('', views_user.landing_page, name='landing'),
    path('register/', views_user.register, name="create_user"),
    path('update/<str:pk>/', views_user.update_account, name="update-account"),
    path('deactivate/<str:pk>/', views_user.deactivate_account, name="deactivate-user"),

    path('archive_page/', views_user.archive_landing, name="archive-landing"),
    path('archive_page/restore/<str:pk>/', views_user.reactivate_account, name="restore-user"),

    path('profile/<str:pk>/', views_user.deactivate_account, name="profile-user"),
    path('profile/', views_profile.landing_page, name="profile"),
    path('profile/upload-pic', views_profile.upload_profile_pic, name="profile-upload-pic"),

    path('activities/', views_activities.admin_activities, name="admin-activity-log"),
    path('activities/', views_activities.user_activities, name="user-activity-log"),

    path('groups/', views_user_groups.landing, name="user-groups"),
    path('groups/create/', views_user_groups.CreateUserGroups.as_view(), name="user-groups-create"),
    path('groups/archive/<str:pk>/', views_user_groups.archive, name="user-groups-archive"),
    path('groups/restore/<str:pk>/', views_user_groups.restore, name="user-groups-restore"),
    path('groups/destroy/<str:pk>/', views_user_groups.destroy, name="user-groups-destroy"),
    path('groups/archive-page/', views_user_groups.archive_landing, name="user-groups-archive-page"),







]
