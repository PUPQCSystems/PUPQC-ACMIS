from django.urls import path
from . import views_program, views_archive

app_name = 'programs'

urlpatterns = [
    path('', views_program.landing_page, name='landing'),
    path('create/', views_program.create_program, name='create'),
    path('update/<str:pk>/', views_program.update_program, name='update'),
    path('archive/<str:pk>/', views_program.archive_program, name='archive'),
    path('restore/<str:pk>/', views_archive.restore_program, name='restore'),
    path('destroy/<str:pk>/', views_archive.destroy_program, name='destroy'),
    path('archive_page/', views_archive.landing_page, name='archive-landing'),

]
