from django.urls import path
from Accreditation import views_instrument_level, views_component_indicator
from Accreditation import views_component
from Accreditation.views_component import ComponentList
from Accreditation.views_component_indicator import ParameterIndicatorList
from . import views_accreditation, views_level, views_type, views_bodies, views_instrument, views_area, views_level_area, views_parameter, views_area_parameter
from Accreditation.views_instrument import *
from Accreditation.views_instrument_level import *
from Accreditation.views_level_area import *
from Accreditation.views_area import *
from Accreditation.views_parameter import *
from Accreditation.views_area_parameter import *
from Accreditation.views_component_indicator import *


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

    path("area/", AreaList.as_view(), name='area-landing'),
    path("area/update/<int:pk>/", views_area.update, name='area-update'),
    path("area/archive/<int:pk>/", views_area.archive, name='area-archive'),
    path("area/archive-page/", views_area.archive_landing, name='area-archive-page'),
    path("area/archive-page/restore/<int:pk>/", views_area.restore, name='area-restore'),
    path("area/archive-page/destroy/<int:pk>/", views_area.destroy, name='area-destroy'),

    path("parameter/", ParameterList.as_view(), name='parameter-landing'),
    path("parameter/update/<int:pk>/", views_parameter.update, name='parameter-update'),
    path("parameter/archive/<int:pk>/", views_parameter.archive, name='parameter-archive'),
    path("parameter/archive-page/", views_parameter.archive_landing, name='parameter-archive-page'),
    path("parameter/archive-page/restore/<int:pk>/", views_parameter.restore, name='parameter-restore'),
    path("parameter/archive-page/destroy/<int:pk>/", views_parameter.destroy, name='parameter-destroy'),

    path("component/", ComponentList.as_view(), name='component-landing'),
    path("component/update/<int:pk>/", views_component.update, name='component-update'),
    path("component/archive/<int:pk>/", views_component.archive, name='component-archive'),
    path("component/archive-page/", views_component.archive_landing, name='component-archive-page'),
    path("component/archive-page/restore/<int:pk>/", views_component.restore, name='component-restore'),
    path("component/archive-page/destroy/<int:pk>/", views_component.destroy, name='component-destroy'),

    path("bodies/", views_bodies.landing_page, name='bodies-landing'),
    path("bodies/create/", views_bodies.create_bodies, name='bodies-create'),
    path("bodies/update/<str:pk>/", views_bodies.update_bodies, name='bodies-update'),
    path("bodies/archive/<str:pk>/", views_bodies.archive_bodies, name='bodies-archive'),
    path("bodies/archive_page/", views_bodies.archive_landing, name='bodies-archive-page'),
    path("bodies/archive_page/restore/<str:pk>/", views_bodies.restore_bodies, name='bodies-archive-page-restore'),
    path("bodies/archive_page/destroy/<str:pk>/", views_bodies.destroy_bodies, name='bodies-archive-page-destroy'),

    path("instrument/", InstrumentList.as_view(), name='instrument-list'),
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

    path("instrument/level/area/<str:pk>/", LevelAreaList.as_view(), name='instrument-level-area'),
    path("instrument/level/area/create/<int:pk>/", LevelAreaList.as_view(), name='instrument-level-area-create'),
    path("instrument/level/area/update/<str:pk>/", views_level_area.update, name='instrument-level-area-update'),
    path("instrument/level/area/archive/<str:ins_pk>/<str:pk>/", views_level_area.archive, name='instrument-level-area-archive'),
    path("instrument/level/area/<str:pk>/archive-page/", views_level_area.archive_landing, name='instrument-level-area-archive-page'),
    path("instrument/level/area/archive-page/restore/<str:ins_pk>/<str:pk>/", views_level_area.restore, name='instrument-level-area-restore'),
    path("instrument/level/area/archive-page/destroy/<str:pk>/", views_level_area.destroy, name='instrument-level-area-destroy'),

    path("instrument/level/area/parameter/<str:pk>/", AreaParameterList.as_view(), name='instrument-level-area-parameter'),
    path("instrument/level/area/parameter/create/<int:pk>/", CreataAreaParameter.as_view(), name='instrument-level-area-parameter-create'),
    path("instrument/level/area/parameter/update/<str:pk>/", views_area_parameter.update, name='instrument-level-area-parameter-update'),
    path("instrument/level/area/parameter/archive/<str:ins_pk>/<str:pk>/", views_area_parameter.archive, name='instrument-level-area-parameter-archive'),
    path("instrument/level/area/parameter/<str:pk>/archive-page/", views_area_parameter.archive_landing, name='instrument-level-area-parameter-archive-page'),
    path("instrument/level/area/parameter/archive-page/restore/<str:ins_pk>/<str:pk>/", views_area_parameter.restore, name='instrument-level-area-parameter-restore'),
    path("instrument/level/area/parameter/archive-page/destroy/<str:pk>/", views_area_parameter.destroy, name='instrument-level-area-parameter-destroy'),

    path("instrument/level/area/parameter/indicator/<str:pk>/", ParameterIndicatorList.as_view(), name='instrument-parameter-indicator'),
    path("instrument/level/area/parameter/indicator/create-component/<int:pk>/", views_component_indicator.create_component, name='instrument-parameter-component-create'),
    path("instrument/level/area/parameter/indicator/create-indicator/<int:pk>/", views_component_indicator.create_indicator, name='instrument-parameter-indicator-create'),
    path("instrument/level/area/parameter/indicator/create-subindicator/<int:comp_pk>/<int:ind_pk>/", views_component_indicator.create_subindicator, name='instrument-parameter-subindicator-create'),
    path("instrument/level/area/parameter/indicator/update/<str:pk>/", views_component_indicator.update_indicator, name='instrument-parameter-indicator-update'),
    path("instrument/level/area/parameter/indicator/update-component/<str:pk>/", views_component_indicator.update_component, name='instrument-parameter-component-update'),
    path("instrument/level/area/parameter/indicator/archive-indicator/<str:url_pk>/<str:record_pk>/", views_component_indicator.archive_indicator, name='instrument-parameter-indicator-archive'),
    path("instrument/level/area/parameter/indicator/archive-component/<str:url_pk>/<str:record_pk>/", views_component_indicator.archive_component, name='instrument-parameter-component-archive'),
    path("instrument/level/area/parameter/indicator/<str:pk>/archive-page/", views_component_indicator.archive_landing, name='instrument-parameter-indicator-archive-page'),
    path("instrument/level/area/parameter/indicator/archive-page/restore/<str:ins_pk>/<str:pk>/", views_component_indicator.restore, name='instrument-parameter-indicator-restore'),
    path("instrument/level/area/parameter/indicator/archive-page/destroy/<str:pk>/", views_component_indicator.destroy, name='instrument-parameter-indicator-destroy'),

]