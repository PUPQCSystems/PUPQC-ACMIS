from django.db import IntegrityError
from django.utils import timezone
from django.views import View
from rest_framework import generics, viewsets, status
from django.shortcuts import render, redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import Group, Permission
from Users.models import CustomUser, activity_log
from .models import instrument, instrument_level, instrument_level_area, program_accreditation #Import the model for data retieving
from Accreditation.serializers import InstrumentSerializer
from .forms import Create_Instrument_Form, Create_InstrumentLevel_Form, Create_LevelArea_Form, LevelAreaFormSet
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required("Accreditation.view_instrument_level_area", raise_exception=True)
def landing_page(request, pk, accred_pk):
    formset  = LevelAreaFormSet(queryset=instrument_level_area.objects.none())
    records = instrument_level_area.objects.select_related('instrument_level').select_related('area').filter(instrument_level=pk, is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable
    accred_program = program_accreditation.objects.select_related('instrument_level', 'program').get(id=accred_pk)
    user_records = CustomUser.objects.filter(is_active = True)
    # group = Group.objects.get(id=auth_group_id)

    # Initialize an empty list to store update forms for each record
    details = []

    # Iterate through each record and create an update form for it
    for record in records:
        update_form = Create_LevelArea_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form, created_by, modified_by))

    context = { 'records': records,
                'details': details, 
                'pk': pk,   
                'area_formset': formset, 
                'user_records': user_records,
                'accred_program': accred_program
                }  #Getting all the data inside the type table and storing it to the context variable

    return render(request, 'accreditation-page/instrument-area/main-page/landing-page.html', context)

@login_required
@permission_required("Accreditation.delete_instrument_level_area", raise_exception=True)
def archive(request, ins_pk, pk):
    # Gets the records who have this ID
    level_area = instrument_level_area.objects.get(id=pk)

    #After getting that record, this code will delete it.
    level_area.modified_by = request.user
    level_area.is_deleted=True
    level_area.deleted_at = timezone.now()
    name = level_area.area
    level_area.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "ACCREDITATION LEVEL AREA MODULE"
    activity_log_entry.action = "Archived a record"
    activity_log_entry.type = "ARCHIVE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'{name} is successfully archived!') 
    return redirect('accreditations:program-accreditation-area', pk=ins_pk)

#------------------------------------------------------------[ ARCHIVE PAGE CODES ]------------------------------------------------------------#
@login_required
@permission_required("Accreditation.delete_instrument_level_area", raise_exception=True)
def archive_landing(request, pk):
    records = instrument_level_area.objects.select_related('instrument_level').select_related('area').filter(instrument_level=pk, is_deleted= True) #Getting all the data inside the Program table and storing it to the context variable

    details = []
     # Iterate through each record and create an update form for it
    for record in records:
        update_form =  Create_LevelArea_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form,created_by, modified_by))

    context = { 'details': details, 'pk': pk , 'records': records}#Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-page/instrument-area/archive-page/landing-page.html', context)

@login_required
@permission_required("Accreditation.delete_instrument_level_area", raise_exception=True)
def restore(request, ins_pk, pk):
    # Gets the records who have this ID
    level_area = instrument_level_area.objects.get(id=pk)

    #After getting that record, this code will restore it.
    level_area.modified_by = request.user
    level_area.deleted_at = None
    level_area.is_deleted=False
    name = level_area.area
    level_area.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "ACCREDITATION LEVEL AREA MODULE"
    activity_log_entry.action = "Restored a record"
    activity_log_entry.type = "RESTORE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'{name} is successfully restored!') 
    return redirect('accreditations:program-accreditation-area-archive-page', pk=ins_pk)
