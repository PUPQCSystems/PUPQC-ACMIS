from django.urls import path
from . import views_accreditation, views_type

urlpatterns = [

    path("accreditation_page/", views_accreditation.landing_page, name='accreditation-landing'),


    path("accreditation_type/", views_type.landing_page, name='accreditation-type-landing'),
    path("accreditation_type/create/", views_type.create_type, name='accreditation-type-create'),
    path("accreditation_type/update/<str:pk>/", views_type.update_type, name='accreditation-type-update'),
    path("accreditation_type/archive/<str:pk>/", views_type.archive_type, name='accreditation-type-archive'),

    path("accreditation_type/archive_page/", views_type.archive_type_page, name='accreditation-type-archive-page'),
    path("accreditation_type/archive_page/restore/<str:pk>", views_type.restore_type, name='accreditation-type-archive-page-restore'),
    path("accreditation_type/archive_page/destroy/<str:pk>", views_type.destroy_type, name='accreditation-type-archive-page-destroy'),

]
