from django.urls import path
from . import views_accreditation, views_level, views_type, views_bodies

urlpatterns = [

    path("accreditation_page/", views_accreditation.landing_page, name='accreditation-landing'),

    path("accreditation_type/", views_type.landing_page, name='accreditation-type-landing'),
    path("accreditation_type/create/", views_type.create_type, name='accreditation-type-create'),
    path("accreditation_type/update/<str:pk>/", views_type.update_type, name='accreditation-type-update'),
    path("accreditation_type/archive/<str:pk>/", views_type.archive_type, name='accreditation-type-archive'),

    path("accreditation_type/archive_page/", views_type.archive_type_page, name='accreditation-type-archive-page'),
    path("accreditation_type/archive_page/restore/<str:pk>", views_type.restore_type, name='accreditation-type-archive-page-restore'),
    path("accreditation_type/archive_page/destroy/<str:pk>", views_type.destroy_type, name='accreditation-type-archive-page-destroy'),

    path("accreditation_level/", views_level.landing_page, name='accreditation-level-landing'),
    path("accreditation_level/create/", views_level.create_level, name='accreditation-level-create'),
    path("accreditation_level/update/<str:pk>/", views_level.update_level, name='accreditation-level-update'),
    path("accreditation_level/archive/<str:pk>/", views_level.archive_level, name='accreditation-level-archive'),

    path("accreditation_level/archive_page/", views_level.archive_level_page, name='accreditation-level-archive-page'),
    path("accreditation_level/archive_page/restore/<str:pk>", views_level.restore_level, name='accreditation-level-archive-page-restore'),
    path("accreditation_level/archive_page/destroy/<str:pk>", views_level.destroy_level, name='accreditation-level-archive-page-destroy'),

    path("accreditation_bodies/", views_bodies.landing_page, name='accreditation-bodies-landing'),
    path("accreditation_bodies/create/", views_bodies.create_bodies, name='accreditation-bodies-create'),
    path("accreditation_bodies/update/<str:pk>/", views_bodies.update_bodies, name='accreditation-bodies-update'),
    path("accreditation_bodies/archive/<str:pk>/", views_bodies.archive_bodies, name='accreditation-bodies-archive'),

    path("accreditation_bodies/archive_page/", views_bodies.archive_landing, name='accreditation-bodies-archive-page'),
    path("accreditation_bodies/archive_page/restore/<str:pk>", views_bodies.restore_bodies, name='accreditation-bodies-archive-page-restore'),
    path("accreditation_bodies/archive_page/destroy/<str:pk>", views_bodies.destroy_bodies, name='accreditation-bodies-archive-page-destroy'),

]
