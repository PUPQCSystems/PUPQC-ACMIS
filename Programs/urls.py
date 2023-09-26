from django.urls import path
from . import views_program, views_archive, views_accreditation

urlpatterns = [
    path("program_page/", views_program.landing_page, name='program-landing'),
    path("program_create/", views_program.create_program, name='program-create'),
    path("program_update/<str:pk>/", views_program.update_program, name='program-update'),
    path("program_archive/<str:pk>/", views_program.archive_program, name='program-archive'),
    path("program_restore/<str:pk>/", views_archive.restore_program, name='program-restore'),
    path("program_destroy/<str:pk>/", views_archive.destroy_program, name='program-destroy'),
    path("archive_page/", views_archive.landing_page, name='archive-landing'),

    path("accreditation_page/", views_accreditation.landing_page, name='accreditation-landing'),

]
