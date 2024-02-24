from django.db import IntegrityError
from django.utils import timezone
from django.views import View

from django.shortcuts import render, redirect, render, get_object_or_404
from django.http import  JsonResponse

from Users.models import activity_log
from .models import component_upload_bin, instrument_level, instrument_level_area, level_area_parameter, parameter_components #Import the model for data retieving
from Accreditation.serializers import InstrumentSerializer
from .forms import AreaParameterFormSet, AreaParameter_Form
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


class AreaParameterList(View):
    def get(self, request, pk):
        #Getting the data from the API
        area_detail = instrument_level_area.objects.get(id=pk)
        records = level_area_parameter.objects.select_related('instrument_level_area').select_related('parameter').filter(instrument_level_area=pk, is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable

        # Initialize an empty list to store update forms for each record
        details = []

        # Iterate through each record and create an update form for it
        for record in records:
            update_form = AreaParameter_Form(instance=record)
            created_by = record.created_by  # Get the user who created the record
            modified_by = record.modified_by  # Get the user who modified the record
            details.append((record, update_form, created_by, modified_by))

        context = { 'records': records,'details': details, 'pk': pk, 'area_detail': area_detail}  #Getting all the data inside the type table and storing it to the context variable

        return render(request, 'accreditation-level-area-parameter/main-page/landing-page.html', context)        

class CreatAreaParameter(View):
    def get(self, request, pk):
        #Getting the data from the API
        formset  = AreaParameterFormSet(queryset=level_area_parameter.objects.none())
       
        context = {'formset': formset, 'pk': pk}  #Getting all the data inside the type table and storing it to the context variable
        return render(request, 'accreditation-level-area-parameter/main-page/create-page.html', context)
    

    def post(self, request, pk):
        formset = AreaParameterFormSet(data=self.request.POST)
        instrument_area_id = pk  # assign the instrument_level ID

        try:
            if formset.is_valid():
                for form in formset:
                    form.instance.instrument_level_area_id = instrument_area_id
                    form.instance.created_by = request.user
                formset.save()  # Save the formset with the assigned foreign keys

                # Create an instance of the ActivityLog model
                activity_log_entry = activity_log()

                # Set the attributes of the instance
                activity_log_entry.module = "AREA PARAMETER MODULE"
                activity_log_entry.action = "Created record/s"
                activity_log_entry.type = "CREATE"
                activity_log_entry.datetime_acted =  timezone.now()
                activity_log_entry.acted_by = request.user
                # Set other attributes as needed

                # Save the instance to the database
                activity_log_entry.save()
                redirect_url= f'/accreditation/instrument/level/area/parameter/{pk}/'
                messages.success(request, f"Parameters are successfully created!")
                return JsonResponse({'status': 'success', 'redirect_url': redirect_url}, status=200)
            else:
                return JsonResponse({'errors': formset.errors}, status=400)
            
        except IntegrityError as e:
            # Handle the IntegrityError here
            return JsonResponse({'error': 'Error: There might be a selected parameter that is already exists. Please make sure that the parameters are different and no parameter is repeatedly selected.'}, status=400)

@login_required
def update(request, pk):
# Retrieve the type object with the given primary key (pk)
    
    try:
        area_parameter = level_area_parameter.objects.get(id=pk)
    except level_area_parameter.DoesNotExist:
        return JsonResponse({'errors': 'Parameter not found'}, status=404)

    if request.method == 'POST':
        # Process the form submission with updated data
        update_form =  AreaParameter_Form(request.POST or None, instance = area_parameter)
        try:
            if update_form.is_valid():
                # Save the updated data to the database
                update_form.instance.modified_by = request.user
                name = area_parameter.parameter
                update_form.save()  

                # Create an instance of the ActivityLog model
                activity_log_entry = activity_log()

                # Set the attributes of the instance
                activity_log_entry.module = "AREA PARAMETER MODULE"
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
            return JsonResponse({'error': 'Error: There might be a selected parameter that is already exists. Please make sure that the parameters are different and no parameter is repeatedly selected.'}, status=400)
        
@login_required
def archive(request, ins_pk, pk):
    # Gets the records who have this ID
    area_parameter = level_area_parameter.objects.get(id=pk)

    #After getting that record, this code will delete it.
    area_parameter.modified_by = request.user
    area_parameter.is_deleted=True
    area_parameter.deleted_at = timezone.now()
    name = area_parameter.parameter
    area_parameter.save()

# ----------------------------------[ Calculating the progress percentage per each instrument_areas ]--------------------------------------
    # Get the area record
    area_record = instrument_level_area.objects.select_related('instrument_level').get(id=area_parameter.instrument_level_area_id)

    # Get all child parameters of the area that are not soft deleted
    area_parameters = level_area_parameter.objects.filter(instrument_level_area_id=area_record.id, is_deleted=False)
    if area_parameters.exists():
        # Initialize counters
        all_area_bins = 0
        approved_area_bins = 0

        # Iterate through each parameter
        for parameter in area_parameters:
            # Get all child parameter_components of the parameter that are NOT soft deleted
            area_parameter_components = parameter_components.objects.filter(area_parameter_id=parameter.id, is_deleted=False)

            # Count all and approved bins for each component that are not soft deleted
            all_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components, is_deleted=False).count()
            approved_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components, status="approve", is_deleted=False).count()

            # Increment counters
            all_area_bins += all_bins
            approved_area_bins += approved_bins

        # Calculate progress
        progress = 0.00
        if all_area_bins:
            progress = (approved_area_bins / all_area_bins) * 100

            # Update the progress_percentage field of the area record
            area_record.progress_percentage = progress
            area_record.save()
        
        else:
            area_record.progress_percentage = 0.00
            area_record.save()
        
    else:
        area_record.progress_percentage = 0.00
        area_record.save()

#----------------[ Codes for calculating program percentage of the program accreditation/ instument_level ]----------------

    instrument_id = area_record.instrument_level.id
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
    return redirect('accreditations:instrument-level-area-parameter', pk=ins_pk)

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
    return render(request, 'accreditation-level-area-parameter/archive-page/landing-page.html', context)

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

# ----------------------------------[ Calculating the progress percentage per each instrument_areas ]--------------------------------------
    # Get the area record
    area_record = instrument_level_area.objects.select_related('instrument_level').get(id=area_parameter.instrument_level_area_id)

    # Get all child parameters of the area that are not soft deleted
    area_parameters = level_area_parameter.objects.filter(instrument_level_area_id=area_record.id, is_deleted=False)

    # Initialize counters
    all_area_bins = 0
    approved_area_bins = 0

    # Iterate through each parameter
    for parameter in area_parameters:
        # Get all child parameter_components of the parameter that are NOT soft deleted
        area_parameter_components = parameter_components.objects.filter(area_parameter_id=parameter.id, is_deleted=False)

        # Count all and approved bins for each component that are not soft deleted
        all_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components, is_deleted=False).count()
        approved_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components, status="approve", is_deleted=False).count()

        # Increment counters
        all_area_bins += all_bins
        approved_area_bins += approved_bins

    # Calculate progress
    progress = 0.00
    if all_area_bins:
        progress = (approved_area_bins / all_area_bins) * 100

        # Update the progress_percentage field of the area record
        area_record.progress_percentage = progress
        area_record.save()

#----------------[ Codes for calculating program percentage of the program accreditation/ instument_level ]----------------

    instrument_id = area_record.instrument_level.id
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
    activity_log_entry.module = "AREA PARAMETER MODULE"
    activity_log_entry.action = "Restored a record"
    activity_log_entry.type = "RESTORE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'{name} is successfully restored!') 
    return redirect('accreditations:instrument-level-area-parameter-archive-page', pk=ins_pk)

@login_required
def destroy(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                area_parameter = level_area_parameter.objects.get(id=pk)
                name = area_parameter.parameter  #Get the name of the record

                #After getting that record, this code will delete it.
                area_parameter.delete()

                # Create an instance of the ActivityLog model
                activity_log_entry = activity_log()

                # Set the attributes of the instance
                activity_log_entry.module = "AREA PARAMETER MODULE"
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