from django.urls import path
from Accreditation import  views_accreditation, views_assign_user, views_instrument_folder, views_instrument_level, views_submission_bin
from . import views_level, views_bodies, views_instrument

from Accreditation.views_instrument_level import *

app_name = 'accreditations'

urlpatterns = [

    #------------------------------[ URLS FOR ACCREDITATION LEVEL MODULE ]------------------------------#
    path("level/", views_level.landing_page, name='level-landing'),
    path("level/create/", views_level.create_level, name='level-create'),
    path("level/update/<str:pk>/", views_level.update_level, name='level-update'),
    path("level/archive/<str:pk>/", views_level.archive_level, name='level-archive'),
    path("level/archive_page/", views_level.archive_level_page, name='level-archive-page'),
    path("level/archive_page/restore/<str:pk>/", views_level.restore_level, name='level-archive-page-restore'),
    path("level/archive_page/destroy/<str:pk>/", views_level.destroy_level, name='level-archive-page-destroy'),

    
    #------------------------------[ URLS FOR ACCREDITATION BODIES MODULE ]------------------------------#
    path("bodies/", views_bodies.landing_page, name='bodies-landing'),
    path("bodies/create/", views_bodies.create_bodies, name='bodies-create'),
    path("bodies/update/<str:pk>/", views_bodies.update_bodies, name='bodies-update'),
    path("bodies/archive/<str:pk>/", views_bodies.archive_bodies, name='bodies-archive'),
    path("bodies/archive_page/", views_bodies.archive_landing, name='bodies-archive-page'),
    path("bodies/archive_page/restore/<str:pk>/", views_bodies.restore_bodies, name='bodies-archive-page-restore'),
    path("bodies/archive_page/destroy/<str:pk>/", views_bodies.destroy_bodies, name='bodies-archive-page-destroy'),
    
    #------------------------------[ URLS FOR INSTRUMENT MODULE]------------------------------#
    path("instrument/", views_instrument.InstrumentList.as_view(), name='instrument-list'),
    path("instrument/update/<str:pk>/", views_instrument.update, name='instrument-update'),
    path("instrument/archive/<str:pk>/", views_instrument.archive, name='instrument-archive'),
    path("instrument/archive_page/", views_instrument.archive_landing, name='instrument-archive-page'),
    path("instrument/archive_page/restore/<str:pk>/", views_instrument.restore, name='instrument-restore'),
    path("instrument/archive_page/destroy/<str:pk>/", views_instrument.destroy, name='instrument-destroy'),

    #------------------------------[ URLS FOR INSTRUMENT LEVEL ]------------------------------#
    path("instrument/level/<str:pk>/", InstrumentLevelList.as_view(), name='instrument-level'),
    path("instrument/level/create/<int:pk>/", InstrumentLevelList.as_view(), name='instrument-level-create'),
    path("instrument/level/update/<str:pk>/", views_instrument_level.update, name='instrument-level-update'),
    path("instrument/level/archive/<str:ins_pk>/<str:pk>/", views_instrument_level.archive, name='instrument-level-archive'),
    path("instrument/level/<str:pk>/archive-page/", views_instrument_level.archive_landing, name='instrument-level-archive-page'),
    path("instrument/level/archive-page/restore/<str:ins_pk>/<str:pk>/", views_instrument_level.restore, name='instrument-level-restore'),
    path("instrument/level/archive-page/destroy/<str:pk>/", views_instrument_level.destroy, name='instrument-level-destroy'),

    #------------------------------[ URLS FOR PARENT FOLDER ]------------------------------#
    path("instrument/level/directory/<str:pk>/", views_instrument_folder.parent_landing_page, name='instrument-level-directory'),
    path("instrument/level/directory/create/<str:pk>/", views_instrument_folder.create, name='instrument-directory-create'),
    path("instrument/level/directory/update/<str:pk>/", views_instrument_folder.update, name='instrument-directory-update'),
    path("instrument/level/directory/archive/<str:pk>/<str:level_id>/", views_instrument_folder.archive, name='instrument-directory-archive'),
    path("instrument/level/parent-directory/file/archive/<str:pk>/", views_instrument_folder.archive_files, name='parent-directory-file-archive'),
    path("instrument/level/parent-directory/recycle-bin/<str:pk>/", views_instrument_folder.parent_recycle_bin, name='parent-folder-recycle-bin'),
    path("instrument/level/parent-directory/recycle-bin/restore/<str:ins_pk>/<str:pk>/", views_instrument_folder.restore_parent, name='parent-directory-recycle-bin-restore'),
    path("instrument/level/parent-directory/recycle-bin/destroy/<str:pk>/", views_instrument_level.destroy, name='parent-directory-recycle-bin-destroy'),
    path("instrument/level/parent-directory/upload-files/<str:pk>/", views_submission_bin.create_parent_folder_files, name='parent-folder-files-upload'),
    path("instrument/level/directory/recycle-bin/destroy/<str:pk>/", views_instrument_folder.destroy, name='folder-destroy'),


    #------------------------------[ URLS FOR CHILD FOLDER ]------------------------------#
    path("instrument/level/child/directory/<str:pk>/", views_instrument_folder.child_landing_page, name='instrument-level-child-directory'),
    path("instrument/level/child/directory/create/<str:pk>/", views_instrument_folder.create_child, name='instrument-directory-create-child'),
    path("instrument/level/child/directory/archive/<str:pk>/<str:parent_id>/", views_instrument_folder.archive_child, name='instrument-directory-archive-child'),
    path("instrument/level/child-directory/recycle-bin/<str:pk>/", views_instrument_folder.child_recycle_bin, name='child-folder-recycle-bin'),
    path("instrument/level/child-directory/recycle-bin/restore/<str:parent_pk>/<str:pk>/", views_instrument_folder.restore_child, name='child-directory-recycle-bin-restore'),
    path("instrument/level/child-directory/recycle-bin/restore-file/<str:pk>/", views_instrument_folder.restore_child_file, name='child-file-restore'),
    path("instrument/level/child-directory/upload-files/<str:pk>/", views_submission_bin.create_child_folder_files, name='child-folder-files-upload'),


    #------------------------------[ URLS FOR SUBMISSION BIN ]------------------------------#
    path("instrument/level/directory/submission-bin/<str:pk>/", views_submission_bin.landing_page, name='submission-bin-page'),
    path("instrument/level/parent-directory/create/submission-bin/<str:pk>/", views_submission_bin.create_submissionBin_parent, name='create-parent-submission-bin'),
    path("instrument/level/child-directory/create/submission-bin/<str:pk>/", views_submission_bin.create_submissionBin_child, name='create-child-submission-bin'),
    path("instrument/level/directory/submission-bin/update/<str:pk>/", views_submission_bin.update, name='instrument-directory-update'),
    path("instrument/level/directory/submission-bin/upload-files/<str:pk>/", views_submission_bin.create_files, name='files-upload'),
    path("instrument/level/directory/submission-bin/archive/<str:pk>/<str:bin_id>/", views_submission_bin.archive, name='file-archive'),
    path("instrument/level/directory/submission-bin/recycle-bin/<str:pk>/", views_submission_bin.recycle_bin, name='submission-bin-recycle-bin-page'),
    path("instrument/level/directory/submission-bin/recycle-bin/restore/<str:pk>/", views_submission_bin.restore, name='file-restore'),
    path("instrument/level/directory/submission-bin/recycle-bin/destroy/<str:pk>/", views_submission_bin.destroy, name='file-destroy'),


    #------------------------------[ URLS FOR PROGRAM ACCREDITATION ]------------------------------#
    path("filter-instrument-option/", views_accreditation.filter_instrument, name='filter-instument-option'),

    path("", views_accreditation.landing_page, name='landing'),
    path("create/", views_accreditation.create, name='accreditation-create'),
    path("update/<str:pk>/", views_accreditation.update, name='accreditation-update'),
    path("archive/<str:pk>/", views_accreditation.archive, name='accreditation-archive'),
    path("archive-page/", views_accreditation.archive_landing, name='accreditation-archive-page'),
    path("archive-page/restore/<str:pk>/", views_accreditation.restore, name='accreditation-restore'),
    path("archive-page/destroy/<str:pk>/", views_accreditation.destroy, name='accreditation-destroy'),
    path("passed-result/<str:pk>/", views_accreditation.result_passed, name='accreditation-result-passed'),
    path("failed-result/<str:pk>/", views_accreditation.result_failed, name='accreditation-result-failed'),
    path("revisit-result/<str:pk>/", views_accreditation.result_revisit, name='accreditation-result-revisit'),
    path("certificate/destroy/<str:pk>/", views_accreditation.certificate_destroy, name='accreditation-certificate-destroy'),
    path("result-page/<str:pk>/", views_accreditation.result_page, name='accreditation-result-page'),

    path("directory/assign-user/", views_assign_user.assign_user, name='folder-assign-user'),










    



]