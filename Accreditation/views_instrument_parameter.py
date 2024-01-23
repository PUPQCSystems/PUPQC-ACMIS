from django.db import IntegrityError
from django.utils import timezone
from django.views import View
from django.shortcuts import render, redirect, render, get_object_or_404
from django.http import  JsonResponse
from Users.models import activity_log
from .models import level_area_parameter #Import the model for data retieving
from .forms import AreaParameter_Form
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

def landing_page(request, pk):
    #Getting the data from the API
    records = level_area_parameter.objects.select_related('instrument_level_area').select_related('parameter').filter(instrument_level_area=pk, is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable

    # Initialize an empty list to store update forms for each record
    details = []

    # Iterate through each record and create an update form for it
    for record in records:
        update_form = AreaParameter_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form, created_by, modified_by))

    context = { 'records': records,'details': details, 'pk': pk}  #Getting all the data inside the type table and storing it to the context variable

    return render(request, 'accreditation-page/instrument-parameter/main-page/landing-page.html', context)        

@login_required
def archive(request, ins_pk, pk):
    # Gets the records who have this ID
    area_parameter = level_area_parameter.objects.get(id=pk)

    #After getting that record, this code will delete it.
    area_parameter.modified_by = request.user
    area_parameter.is_deleted=True
    area_parameter.deleted_at = timezone.now()
    name = area_parameter.parameter

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "AREA PARAMETER MODULE"
    activity_log_entry.action = "Archived a record"
    activity_log_entry.type = "ARCHIVE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()
    area_parameter.save()

    messages.success(request, f'{name} is successfully archived!') 
    return redirect('accreditations:program-accreditation-parameter', pk=ins_pk)

#------------------------------------------------------------[ ARCHIVE PAGE CODES ]------------------------------------------------------------#
@login_required
def archive_landing(request, pk):
    records = level_area_parameter.objects.select_related('instrument_level_area').select_related('parameter').filter(instrument_level_area=pk, is_deleted= True) #Getting all the data inside the Program table and storing it to the context variable

    details = []
     # Iterate through each record and create an update form for it
    for record in records:
        update_form =  AreaParameter_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form,created_by, modified_by))

    context = { 'details': details, 'pk': pk , 'records': records}#Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-page/instrument-parameter/archive-page/landing-page.html', context)

@login_required
def restore(request, ins_pk, pk):
    # Gets the records who have this ID
    area_parameter = level_area_parameter.objects.get(id=pk)

    #After getting that record, this code will restore it.
    area_parameter.modified_by = request.user
    area_parameter.deleted_at = None
    area_parameter.is_deleted=False
    name = area_parameter.parameter
    area_parameter.save()

   # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "AREA PARAMETER MODULE"
    activity_log_entry.action = "Restored a record"
    activity_log_entry.type = "RESTORE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'{name} is successfully restored!') 
    return redirect('accreditations:program-accreditation-parameter-archive-page', pk=ins_pk)