from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.db.models import Sum
from Users.models import activity_log
from .models import component_upload_bin, instrument_level, instrument_level_area, level_area_parameter, parameter_components #Import the model for data retieving
from .forms import UploadBin_Form, ParameterComponent_Form
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
 

class ParameterComponentList(View):

   # Permission for GET requests
    permission_required = "Accreditation.view_parameter_components"

    def get(self, request, pk):
        #Getting the data from the API
        component_form = ParameterComponent_Form(request.POST or None)
        uploadBin_form = UploadBin_Form(request.POST or None)
        component_records = parameter_components.objects.select_related('area_parameter').filter(area_parameter=pk, is_deleted = False)
       
        indicator_details = {}

        for component_record in component_records.values():
            records = []
            #Convert the component_record dictionary into object or queryset
            component = parameter_components(**component_record)

            component_update_form = ParameterComponent_Form(instance=component)

            #Adding the component_update_form key and value into the component_record dictionary
            component_record['component_update_form'] = component_update_form

            #Convert the component_record dictionary back into object or queryset
            component_record = parameter_components(**component_record)

            indicator_records = component_upload_bin.objects.select_related('parameter_component').filter(parameter_component=component_record.id, is_deleted = False)
            if indicator_records:
                for indicator_record in  indicator_records.values():
                    # Convert the dictionary back to a model instance
                    indicator_instance = component_upload_bin(**indicator_record)
                    
                    # Now you can use the instance with the form
                    uploadBin_update_form = UploadBin_Form(instance=indicator_instance)
                    indicator_record['uploadBin_update_form'] = uploadBin_update_form
                    records.append(indicator_record)
            
            indicator_details[component_record] = records
        
        print(indicator_details)

        #Getting all the data inside the Program table and storing it to the context variable      
            
        context = { 'component_records': component_records
                   , 'component_form': component_form
                   , 'uploadBin_form': uploadBin_form
                   , 'pk':pk
                   , 'indicator_details': indicator_details
                   
                   }  #Getting all the data inside the type table and storing it to the context variable

        return render(request, 'accreditation-parameter-component/main-page/landing-page.html', context)
    
@login_required
@permission_required("Accreditation.add_parameter_components", raise_exception=True)
def create_component(request, pk):
    component_form = ParameterComponent_Form(request.POST or None)
    try:
        if component_form.is_valid():
            component_form.instance.area_parameter_id = pk
            component_form.instance.created_by = request.user
            component_form.save()

            # Create an instance of the ActivityLog model
            activity_log_entry = activity_log()

            # Set the attributes of the instance
            activity_log_entry.module = "PARAMETER MODULE"
            activity_log_entry.action = "Created a record"
            activity_log_entry.type = "CREATE"
            activity_log_entry.datetime_acted =  timezone.now()
            activity_log_entry.acted_by = request.user
            # Set other attributes as needed

            # Save the instance to the database
            activity_log_entry.save()

            messages.success(request, f'Parameter Component is successfully created!') 
            return JsonResponse({'status': 'success'}, status=200)
        else:
            # Return a validation error using a JSON response
            return JsonResponse({'errors': component_form.errors}, status=400)
    except IntegrityError as e:
        # Handle the IntegrityError here
        return JsonResponse({'error': 'Error: There might be a selected component that is already exists. Please make sure that the selected component is different and no component is repeatedly selected.'}, status=400)

@login_required
@permission_required("Accreditation.add_component_upload_bin", raise_exception=True)
def create_uploadBin(request,pk):
    indicator_form = UploadBin_Form(request.POST or None)


    all_file_types = ['image/jpeg', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                      'application/vnd.ms-excel', 'application/vnd.ms-powerpoint', 'image/png', 'image/gif', 'image/bmp', 'image/svg+xml', 'image/webp', 
                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 
                      'text/plain', 'audio/mp3', 'video/mp4', 'audio/ogg', 'video/webm', 'application/zip', 'application/x-rar-compressed', 'text/csv', 'text/html', 'text/css', 
                      'application/javascript']
    
    if indicator_form.is_valid():
        indicator_form.instance.parameter_component_id = pk
        indicator_form.instance.created_by = request.user
        # indicator_form.instance.accepted_file_type = request.POST.getlist('accepted_file_type')
        indicator_form.instance.accepted_file_type = all_file_types

        # indicator_form.instance.accepted_file_count = request.POST.get('accepted_file_count')
        indicator_form.instance.accepted_file_count = 10
        # indicator_form.instance.accepted_file_size = request.POST.get('accepted_file_size')
        indicator_form.instance.accepted_file_size = 1000
        indicator_form.save()

        # Create an instance of the ActivityLog model
        activity_log_entry = activity_log()

        # Set the attributes of the instance
        activity_log_entry.module = "PARAMETER MODULE"
        activity_log_entry.action = "Created a record"
        activity_log_entry.type = "CREATE"
        activity_log_entry.datetime_acted =  timezone.now()
        activity_log_entry.acted_by = request.user
        # Set other attributes as needed

        # Save the instance to the database
        activity_log_entry.save()

        
        #----------------[ Codes for calculating program percentage for the component ]----------------#
        progress = 0
        # Get the component record
        component_record = parameter_components.objects.select_related('area_parameter').get(id=pk)

        # Count all and approved upload bins for the component
        all_upload_bins = component_upload_bin.objects.filter(parameter_component_id=pk).count()
        approve_upload_bins = component_upload_bin.objects.filter(parameter_component_id=pk, status="approve").count()

        # Calculate progress for the component
        progress = (approve_upload_bins / all_upload_bins) * 100

        # Update the progress_percentage field of the component record
        component_record.progress_percentage = progress
        component_record.save()

        print("Component Progress:", progress)

        #----------------[ Codes for calculating program percentage for the component ]----------------#
        # Get the parameter record
        parameter_record = level_area_parameter.objects.get(id=component_record.area_parameter_id)

        # Count all and approved upload bins for all child parameter components of the parameter
        all_parameter_bins = component_upload_bin.objects.filter(parameter_component__area_parameter_id=parameter_record.id).count()
        approved_parameter_bins = component_upload_bin.objects.filter(parameter_component__area_parameter_id=parameter_record.id, status="approve").count()

        # Calculate progress for the parameter
        progress=0
        progress = (approved_parameter_bins / all_parameter_bins) * 100

        # Update the progress_percentage field of the parameter record
        parameter_record.progress_percentage = progress
        parameter_record.save()

        print("Parameter Progress:", progress)

        #-------------------------------[ Codes for calculating program percentage of the program accreditation ]---------------------------#
   
        # Get the area record
        area_record = instrument_level_area.objects.select_related('instrument_level').get(id=parameter_record.instrument_level_area_id)

        # Get all child parameters of the area
        area_parameters = level_area_parameter.objects.filter(instrument_level_area_id=area_record.id)

        # Initialize counters
        all_area_bins = 0
        approved_area_bins = 0

        # Iterate through each parameter
        for parameter in area_parameters:
            # Get all child parameter_components of the parameter
            area_parameter_components = parameter_components.objects.filter(area_parameter_id=parameter.id)

            # Count all and approved bins for each component
            all_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components).count()
            approved_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components, status="approve").count()

            # Increment counters
            all_area_bins += all_bins
            approved_area_bins += approved_bins

        # Calculate progress
        progress = (approved_area_bins / all_area_bins) * 100

        # Update the progress_percentage field of the area record
        area_record.progress_percentage = progress
        area_record.save()

        #----------------[ Codes for calculating program percentage of the program accreditation/ instument_level ]----------------
        progress = 0.00
        instrument_id = area_record.instrument_level.id
        instrument_record = instrument_level.objects.get(id = instrument_id)
        # codes for updateing progress percentage of a specific area   
        # Get the area ID of a specific area from the parameter_component record
        area_records_count = instrument_level_area.objects.filter(instrument_level_id = instrument_id).count()
     
        overall_percentage = area_records_count * 100

        percentage_sum = instrument_level_area.objects.filter(instrument_level_id=instrument_id).aggregate(Sum('progress_percentage'))['progress_percentage__sum'] or 0
        print("Percentage Sum: ", percentage_sum)
        progress = (percentage_sum / overall_percentage ) * 100
        instrument_record.progress_percentage = progress
        instrument_record.save()
    
        messages.success(request, f'Parameter Upload Bin is successfully created!') 
        return JsonResponse({'status': 'success'}, status=200)
    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': indicator_form.errors}, status=400)
    

@login_required
@permission_required("Accreditation.change_component_upload_bin", raise_exception=True)
def update_uploadBin(request, pk):
# Retrieve the type object with the given primary key (pk)
    try:
        indicator_record = component_upload_bin.objects.get(id=pk)
    except component_upload_bin.DoesNotExist:
        return JsonResponse({'errors': 'Upload bin not found'}, status=404)

    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = UploadBin_Form(request.POST or None, instance=indicator_record)
        if update_form.is_valid():
            # Save the updated data to the database
            update_form.instance.modified_by = request.user
            update_form.instance.accepted_file_type = request.POST.getlist('accepted_file_type')
            update_form.instance.accepted_file_count = request.POST.get('accepted_file_count')
            update_form.instance.accepted_file_size = request.POST.get('accepted_file_size')
            update_form.save()  

            # Create an instance of the ActivityLog model
            activity_log_entry = activity_log()

            # Set the attributes of the instance
            activity_log_entry.module = "PARAMETER MODULE"
            activity_log_entry.action = "Modified a record"
            activity_log_entry.type = "UPDATE"
            activity_log_entry.datetime_acted =  timezone.now()
            activity_log_entry.acted_by = request.user
            # Set other attributes as needed

            # Save the instance to the database
            activity_log_entry.save()

            # Provide a success message as a JSON response
            messages.success(request, f'Upload bin is successfully updated!') 
            return JsonResponse({'status': 'success'}, status=200)


        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)
        
@login_required
@permission_required("Accreditation.change_parameter_components", raise_exception=True)
def update_component(request, pk):
# Retrieve the type object with the given primary key (pk)
    try:
        component_record = parameter_components.objects.get(id=pk)
    except parameter_components.DoesNotExist:
        return JsonResponse({'errors': 'Component not found'}, status=404)

    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = ParameterComponent_Form(request.POST or None, instance=component_record)
        if update_form.is_valid():
            # Save the updated data to the database
            update_form.instance.modified_by = request.user
            update_form.save()  

            # Create an instance of the ActivityLog model
            activity_log_entry = activity_log()

            # Set the attributes of the instance
            activity_log_entry.module = "PARAMETER MODULE"
            activity_log_entry.action = "Modified a record"
            activity_log_entry.type = "UPDATE"
            activity_log_entry.datetime_acted =  timezone.now()
            activity_log_entry.acted_by = request.user
            # Set other attributes as needed

            # Save the instance to the database
            activity_log_entry.save()

            # Provide a success message as a JSON response
            messages.success(request, f'Component is successfully updated!') 
            return JsonResponse({'status': 'success'}, status=200)


        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)
        
        
@login_required
@permission_required("Accreditation.delete_component_upload_bin", raise_exception=True)
def archive_uploadBin(request, url_pk, record_pk):
    # Gets the records who have this ID
    uploadBin_record = component_upload_bin.objects.get(id=record_pk)

    #After getting that record, this code will delete it.
    uploadBin_record.modified_by = request.user
    uploadBin_record.is_deleted=True
    uploadBin_record.deleted_at = timezone.now()
    uploadBin_record.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "PARAMETER MODULE"
    activity_log_entry.action = "Archived a record"
    activity_log_entry.type = "ARCHIVE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'Upload bin is successfully archived!') 
    return redirect('accreditations:instrument-parameter-component', pk=url_pk)

@login_required
@permission_required("Accreditation.delete_parameter_components", raise_exception=True)
def archive_component(request, url_pk, record_pk):
    # Gets the records who have this ID
    component_record = parameter_components.objects.get(id=record_pk)

    #After getting that record, this code will delete it.
    component_record.modified_by = request.user
    component_record.is_deleted=True
    component_record.deleted_at = timezone.now()
    component_record.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "PARAMETER MODULE"
    activity_log_entry.action = "Archived a record"
    activity_log_entry.type = "ARCHIVE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'Component is successfully archived!') 
    return redirect('accreditations:instrument-parameter-component', pk=url_pk)



#------------------------------------------------------------[ ARCHIVE PAGE CODES ]------------------------------------------------------------#
@login_required
@permission_required("Accreditation.delete_parameter_components", raise_exception=True)
def archive_landing(request, pk):
    component_records = parameter_components.objects.select_related('area_parameter').filter(area_parameter=pk)

    indicator_details = {}

    for component_record in component_records.values():
        records = []
        #Convert the component_record dictionary into object or queryset
        component = parameter_components(**component_record)

        component_update_form = ParameterComponent_Form(instance=component)

        #Adding the component_update_form key and value into the component_record dictionary
        component_record['component_update_form'] = component_update_form

        #Convert the component_record dictionary back into object or queryset
        component_record = parameter_components(**component_record)

        indicator_records = component_upload_bin.objects.select_related('parameter_component').filter(parameter_component=component_record.id)
        if indicator_records:
            for indicator_record in  indicator_records.values():
                # Convert the dictionary back to a model instance
                indicator_instance = component_upload_bin(**indicator_record)
                
                # Now you can use the instance with the form
                uploadBin_update_form = UploadBin_Form(instance=indicator_instance)
                indicator_record['uploadBin_update_form'] = uploadBin_update_form
                records.append(indicator_record)
        
        indicator_details[component_record] = records

    print(indicator_details)

    #Getting all the data inside the Program table and storing it to the context variable      
        
    context = { 'component_records': component_records
                , 'pk':pk
                , 'indicator_details': indicator_details
                
                }  #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-parameter-component/archive-page/landing-page.html', context)


@login_required
@permission_required("Accreditation.delete_parameter_components", raise_exception=True)
def restore_component(request, comp_pk, pk):
    # Gets the records who have this ID
    component_record =  parameter_components.objects.get(id=comp_pk)

    #After getting that record, this code will restore it.
    component_record.modified_by = request.user
    component_record.deleted_at = None
    component_record.is_deleted=False
    component_record.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "PARAMETER MODULE"
    activity_log_entry.action = "Restored a record"
    activity_log_entry.type = "RESTORE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'Component is successfully restored!') 
    return redirect('accreditations:instrument-parameter-component-archive-page', pk=pk)

@login_required
@permission_required("Accreditation.delete_component_upload_bin", raise_exception=True)
def restore_uploadBin(request, upl_pk, pk):
    # Gets the records who have this ID
    uploadBin_record =  component_upload_bin.objects.get(id=upl_pk)

    #After getting that record, this code will restore it.
    uploadBin_record.modified_by = request.user
    uploadBin_record.deleted_at = None
    uploadBin_record.is_deleted=False
    uploadBin_record.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "PARAMETER MODULE"
    activity_log_entry.action = "Restored a record"
    activity_log_entry.type = "RESTORE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'Component is successfully restored!') 
    return redirect('accreditations:instrument-parameter-component-archive-page', pk=pk)


@login_required
@permission_required("Accreditation.delete_parameter_components", raise_exception=True)
def destroy_component(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                component_record =  parameter_components.objects.get(id=pk)

                #After getting that record, this code will delete it.
                component_record.delete()

                # Create an instance of the ActivityLog model
                activity_log_entry = activity_log()

                # Set the attributes of the instance
                activity_log_entry.module = "PARAMETER MODULE"
                activity_log_entry.action = "Permanently deleted a record"
                activity_log_entry.type = "DESTROY"
                activity_log_entry.datetime_acted =  timezone.now()
                activity_log_entry.acted_by = request.user
                # Set other attributes as needed

                # Save the instance to the database
                activity_log_entry.save()

                messages.success(request, f'Component is permanently deleted!') 
                return JsonResponse({'success': True}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
@permission_required("Accreditation.delete_component_upload_bin", raise_exception=True)
def destroy_uploadBin(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                uploadBin_record = component_upload_bin.objects.get(id=pk)

                #After getting that record, this code will delete it.
                uploadBin_record.delete()

                # Create an instance of the ActivityLog model
                activity_log_entry = activity_log()

                # Set the attributes of the instance
                activity_log_entry.module = "PARAMETER MODULE"
                activity_log_entry.action = "Permanently deleted a record"
                activity_log_entry.type = "DESTROY"
                activity_log_entry.datetime_acted =  timezone.now()
                activity_log_entry.acted_by = request.user
                # Set other attributes as needed

                # Save the instance to the database
                activity_log_entry.save()

                messages.success(request, f'Upload bin is permanently deleted!') 
                return JsonResponse({'success': True}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


