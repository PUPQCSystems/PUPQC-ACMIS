from django.urls import path
from Accreditation import  views_instrument_level, views_instrument_level_folder
from . import views_level, views_bodies, views_instrument

from Accreditation.views_instrument_level import *

app_name = 'accreditations'

urlpatterns = [
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

    path("instrument/", views_instrument.InstrumentList.as_view(), name='instrument-list'),
    path("instrument/update/<str:pk>/", views_instrument.update, name='instrument-update'),
    path("instrument/archive/<str:pk>/", views_instrument.archive, name='instrument-archive'),
    path("instrument/archive_page/", views_instrument.archive_landing, name='instrument-archive-page'),
    path("instrument/archive_page/restore/<str:pk>/", views_instrument.restore, name='instrument-restore'),
    path("instrument/archive_page/destroy/<str:pk>/", views_instrument.destroy, name='instrument-destroy'),

    path("instrument/level/<str:pk>/", InstrumentLevelList.as_view(), name='instrument-level'),
    path("instrument/level/create/<int:pk>/", InstrumentLevelList.as_view(), name='instrument-level-create'),
    path("instrument/level/update/<str:pk>/", views_instrument_level.update, name='instrument-level-update'),
    path("instrument/level/archive/<str:ins_pk>/<str:pk>/", views_instrument_level.archive, name='instrument-level-archive'),
    path("instrument/level/<str:pk>/archive-page/", views_instrument_level.archive_landing, name='instrument-level-archive-page'),
    path("instrument/level/archive-page/restore/<str:ins_pk>/<str:pk>/", views_instrument_level.restore, name='instrument-level-restore'),
    path("instrument/level/archive-page/destroy/<str:pk>/", views_instrument_level.destroy, name='instrument-level-destroy'),

    path("instrument/level/directory/<str:pk>/", views_instrument_level_folder.landing_page, name='instrument-level-directory'),
    path("instrument/level/directory/create/<str:pk>/", views_instrument_level_folder.create, name='instrument-directory-create'),
    path("instrument/level/directory/update/<str:pk>/", views_instrument_level.update, name='instrument-directory-update'),
    path("instrument/level/directory/archive/<str:ins_pk>/<str:pk>/", views_instrument_level.archive, name='instrument-directory-archive'),
    path("instrument/level/directory/<str:pk>/archive-page/", views_instrument_level.archive_landing, name='instrument-directory-archive-page'),
    path("instrument/level/directory/archive-page/restore/<str:ins_pk>/<str:pk>/", views_instrument_level.restore, name='instrument-directory-restore'),
    path("instrument/level/directory/archive-page/destroy/<str:pk>/", views_instrument_level.destroy, name='instrument-directory-destroy'),


]