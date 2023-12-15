from django.urls import path
from . import views_accreditation, views_level, views_type, views_bodies, views_instrument
from Accreditation.views_instrument import *



app_name = 'accreditations'

urlpatterns = [

    path("", views_accreditation.landing_page, name='landing'),

    path("type/", views_type.landing_page, name='type-landing'),
    path("type/create/", views_type.create_type, name='type-create'),
    path("type/update/<str:pk>/", views_type.update_type, name='type-update'),
    path("type/archive/<str:pk>/", views_type.archive_type, name='type-archive'),

    path("type/archive_page/", views_type.archive_type_page, name='type-archive-page'),
    path("type/archive_page/restore/<str:pk>/", views_type.restore_type, name='type-archive-page-restore'),
    path("type/archive_page/destroy/<str:pk>/", views_type.destroy_type, name='type-archive-page-destroy'),

    path("level/", views_level.landing_page, name='level-landing'),
    path("level/create/", views_level.create_level, name='level-create'),
    path("level/update/<str:pk>/", views_level.update_level, name='level-update'),
    path("level/archive/<str:pk>/", views_level.archive_level, name='level-archive'),

    path("level/archive_page/", views_level.archive_level_page, name='level-archive-page'),
    path("level/archive_page/restore/<str:pk>/", views_level.restore_level, name='level-archive-page-restore'),
    path("level/archive_page/destroy/<str:pk>/", views_level.destroy_level, name='level-archive-page-destroy'),

    path("bodies/", views_bodies.landing_page, name='bodies-landing'),
    path("bodies/create/", views_bodies.create_bodies, name='bodies-create'),
    path("bodies/update/<str:pk>/", views_bodies.update_bodies, name='bodies-update'),
    path("bodies/archive/<str:pk>/", views_bodies.archive_bodies, name='bodies-archive'),

    path("bodies/archive_page/", views_bodies.archive_landing, name='bodies-archive-page'),
    path("bodies/archive_page/restore/<str:pk>/", views_bodies.restore_bodies, name='bodies-archive-page-restore'),
    path("bodies/archive_page/destroy/<str:pk>/", views_bodies.destroy_bodies, name='bodies-archive-page-destroy'),


    #API CRUD PATHS FOR INTRUMENT MODULE
    path("instrument/", InstrumentList.as_view(), name='instrument-list'),
    path("instrument/update/<str:pk>/", views_instrument.update, name='instrument-update'),
    path("instrument/archive/<str:pk>/", views_instrument.archive, name='instrument-archive'),


    path("instrument/archive_page/", views_instrument.archive_landing, name='instrument-archive-page'),
    path("instrument/archive_page/restore/<str:pk>/", views_instrument.restore, name='instrument-restore'),
    path("instrument/archive_page/destroy/<str:pk>/", views_instrument.destroy, name='instrument-destroy'),






]