from django.db import IntegrityError
from django.utils import timezone
from django.views import View
from django.shortcuts import render, redirect, render, get_object_or_404
from django.http import  JsonResponse
from Users.models import activity_log
from .models import level_area_parameter, parameter_components #Import the model for data retieving
from .forms import AreaParameter_Form
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required


@login_required
@permission_required("Accreditation.view_level_area_parameter", raise_exception=True)
def landing_page(request, pk):
    #Getting the data from the API
    records = level_area_parameter.objects.select_related('instrument_level_area').select_related('parameter').filter(instrument_level_area=pk, is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable
    create_form = AreaParameter_Form(request.POST or None)

    # Initialize an empty list to store update forms for each record
    details = []

    # Iterate through each record and create an update form for it
    for record in records:
        update_form = AreaParameter_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form, created_by, modified_by))

    context = { 'records': records,'details': details, 'pk': pk, 'create_form': create_form}  #Getting all the data inside the type table and storing it to the context variable

    return render(request, 'accreditation-page/instrument-parameter/main-page/landing-page.html', context)   


def create(request,pk):
    create_form = AreaParameter_Form(request.POST or None)
    instrument_area_id = pk  # assign the instrument_level ID

    try:
        if create_form.is_valid():
            create_form.instance.created_by = request.user
            create_form.instance.instrument_level_area_id = instrument_area_id
            create_form.save()

        # Create an instance of the ActivityLog model
            activity_log_entry = activity_log()

            # Set the attributes of the instance
            activity_log_entry.module = "AREA PARAMETER MODULE"
            activity_log_entry.action = "Created a record"
            activity_log_entry.type = "CREATE"
            activity_log_entry.datetime_acted =  timezone.now()
            activity_log_entry.acted_by = request.user
            # Set other attributes as needed

            # Save the instance to the database
            activity_log_entry.save()

            messages.success(request, f'Area Parameter is successfully created!') 
            return JsonResponse({'status': True}, status=201)
        else:
            print("The error: ",create_form.errors)
            # Return a validation error using a JSON response
            return JsonResponse({'errors': create_form.errors}, status=400)
    except IntegrityError as e:
            # Handle the IntegrityError here
            return JsonResponse({'error': 'Error: Duplicate or conflicting instrument parameter. Please choose a unique option.'}, status=400)
    

@login_required
@permission_required("Accreditation.delete_level_area_parameter", raise_exception=True)
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
@permission_required("Accreditation.delete_level_area_parameter", raise_exception=True)
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
@permission_required("Accreditation.delete_level_area_parameter", raise_exception=True)
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