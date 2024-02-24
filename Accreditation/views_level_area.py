from django.db import IntegrityError
from django.utils import timezone
from django.views import View
from rest_framework import generics, viewsets, status
from django.shortcuts import render, redirect, render, get_object_or_404
from django.http import  JsonResponse

from Users.models import activity_log
from .models import component_upload_bin, instrument, instrument_level, instrument_level_area, level_area_parameter, parameter_components #Import the model for data retieving
from Accreditation.serializers import InstrumentSerializer
from .forms import Create_LevelArea_Form, LevelAreaFormSet
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin


class LevelAreaList(PermissionRequiredMixin, View):
    # Permission for GET requests
    permission_required = ["Accreditation.view_instrument_level_area", "Accreditation.add_instrument_level_area"]
    
    def get(self, request, pk):
        #Getting the data from the API
        formset  = LevelAreaFormSet(queryset=instrument_level_area.objects.none())
        records = instrument_level_area.objects.select_related('instrument_level').select_related('area').filter(instrument_level=pk, is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable

        # Initialize an empty list to store update forms for each record
        details = []

        # Iterate through each record and create an update form for it
        for record in records:
            update_form = Create_LevelArea_Form(instance=record)
            created_by = record.created_by  # Get the user who created the record
            modified_by = record.modified_by  # Get the user who modified the record
            details.append((record, update_form, created_by, modified_by))

        context = { 'records': records,'details': details, 'pk': pk, 'area_formset': formset}  #Getting all the data inside the type table and storing it to the context variable

        return render(request, 'accreditation-level-area/main-page/landing-page.html', context)
    
    def post(self, request, pk):
        formset = LevelAreaFormSet(data=self.request.POST)
        instrument_level_id = pk  # assign  the instrument_level ID
        for form in formset:
            form.instance.instrument_level_id = instrument_level_id
            form.instance.created_by = request.user
        try:
    
            if formset.is_valid():
                formset_saved = formset.save()  # Save the formset with the assigned foreign keys

                if formset_saved:
                    # Create an instance of the ActivityLog model
                    activity_log_entry = activity_log()

                    # Set the attributes of the instance
                    activity_log_entry.module = "ACCREDITATION LEVEL AREA MODULE"
                    activity_log_entry.action = "Created a record"
                    activity_log_entry.type = "CREATE"
                    activity_log_entry.datetime_acted =  timezone.now()
                    activity_log_entry.acted_by = request.user
                    # Set other attributes as needed

                    # Save the instance to the database
                    activity_log_entry.save()

                    messages.success(request, f"Instrument's level areas is successfully created!")
                    return JsonResponse({'status': 'success'}, status=200)
                else:
                    return JsonResponse({'error': "The form is empty. Please input a value before submitting."}, status=400)
            else:
                return JsonResponse({'errors': formset.errors}, status=400)
        except IntegrityError as e:
            # Handle the IntegrityError here
            return JsonResponse({'error': 'Error: Duplicate or conflicting selected areas. Please choose a unique option.'}, status=400)

                

@login_required
@permission_required("Accreditation.change_instrument_level_area", raise_exception=True)
def update(request, pk):
# Retrieve the type object with the given primary key (pk)
    try:
        try:
            level_area = instrument_level_area.objects.get(id=pk)
        except instrument.DoesNotExist:
            return JsonResponse({'errors': 'instrument level not found'}, status=404)

        if request.method == 'POST':
            # Process the form submission with updated data
            update_form =  Create_LevelArea_Form(request.POST or None, instance = level_area)
            if update_form.is_valid():
                # Save the updated data to the database
                update_form.instance.modified_by = request.user
                name = level_area.area
                update_form.save()  

                
                # Create an instance of the ActivityLog model
                activity_log_entry = activity_log()

                # Set the attributes of the instance
                activity_log_entry.module = "ACCREDITATION LEVEL AREA MODULE"
                activity_log_entry.action = "Modified a record"
                activity_log_entry.type = "UPDATE"
                activity_log_entry.datetime_acted =  timezone.now()
                activity_log_entry.acted_by = request.user
                # Set other attributes as needed

                # Save the instance to the database
                activity_log_entry.save()

                # Provide a success message as a JSON response
                messages.success(request, f'{name} is successfully updated!') 
                return JsonResponse({'status': 'success'}, status=200)


            else:
                # Return a validation error as a JSON response
                return JsonResponse({'errors': update_form.errors}, status=400)
            
    except IntegrityError as e:
        # Handle the IntegrityError here
        return JsonResponse({'error': 'Error: There might be a selected area that is already exists. Please make sure that the selected area is not existing.'}, status=400)
        
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


#----------------[ Codes for calculating program percentage of the program accreditation/ instument_level ]----------------
    instrument_id = level_area.instrument_level.id
    instrument_record = instrument_level.objects.get(id = instrument_id)

    # Get all child areas of the program accreditation/ instrument level
    areas = instrument_level_area.objects.filter(instrument_level=instrument_record, is_deleted=False)

    # Initialize counters
    all_area_bins = 0
    approved_area_bins = 0
    for area_record in areas:
        # Get all child parameters of the area
        area_parameters = level_area_parameter.objects.filter(instrument_level_area_id=area_record.id, is_deleted=False)

        # Iterate through each parameter
        for parameter in area_parameters:
            # Get all child parameter_components of the parameter
            area_parameter_components = parameter_components.objects.filter(area_parameter_id=parameter.id, is_deleted=False)

            # Count all and approved bins for each component
            all_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components, is_deleted=False).count()
            approved_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components, status="approve", is_deleted=False).count()

            # Increment counters
            all_area_bins += all_bins
            approved_area_bins += approved_bins

    # Calculate progress
    progress = 0.00
    progress = (approved_area_bins / all_area_bins) * 100
    print("Progress: ", progress)
    # Update the progress_percentage field of the area record
    instrument_record.progress_percentage = progress
    instrument_record.save()


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
    return redirect('accreditations:instrument-level-area', pk=ins_pk)

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
    return render(request, 'accreditation-level-area/archive-page/landing-page.html', context)

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

    #----------------[ Codes for calculating program percentage of the program accreditation/ instument_level ]----------------
    instrument_id = level_area.instrument_level.id
    instrument_record = instrument_level.objects.get(id = instrument_id)

    # Get all child areas of the program accreditation/ instrument level
    areas = instrument_level_area.objects.filter(instrument_level=instrument_record, is_deleted=False)

    # Initialize counters
    all_area_bins = 0
    approved_area_bins = 0
    for area_record in areas:
        # Get all child parameters of the area
        area_parameters = level_area_parameter.objects.filter(instrument_level_area_id=area_record.id, is_deleted=False)

        # Iterate through each parameter
        for parameter in area_parameters:
            # Get all child parameter_components of the parameter
            area_parameter_components = parameter_components.objects.filter(area_parameter_id=parameter.id, is_deleted=False)

            # Count all and approved bins for each component
            all_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components, is_deleted=False).count()
            approved_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components, status="approve", is_deleted=False).count()

            # Increment counters
            all_area_bins += all_bins
            approved_area_bins += approved_bins

    # Calculate progress
    progress = 0.00
    progress = (approved_area_bins / all_area_bins) * 100
    print("Progress: ", progress)
    # Update the progress_percentage field of the area record
    instrument_record.progress_percentage = progress
    instrument_record.save()

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
    return redirect('accreditations:instrument-level-area-archive-page', pk=ins_pk)

@login_required
@permission_required("Accreditation.delete_instrument_level_area", raise_exception=True)
def destroy(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                level_area = instrument_level_area.objects.get(id=pk)
                name = level_area.area  #Get the name of the record

                #After getting that record, this code will delete it.
                level_area.delete()

              # Create an instance of the ActivityLog model
                activity_log_entry = activity_log()

                # Set the attributes of the instance
                activity_log_entry.module = "ACCREDITATION LEVEL AREA MODULE"
                activity_log_entry.action = "Permanently deleted a record"
                activity_log_entry.type = "DESTROY"
                activity_log_entry.datetime_acted =  timezone.now()
                activity_log_entry.acted_by = request.user
                # Set other attributes as needed

                # Save the instance to the database
                activity_log_entry.save()


                messages.success(request, f'{name} is permanently deleted!') 
                return JsonResponse({'success': True}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})