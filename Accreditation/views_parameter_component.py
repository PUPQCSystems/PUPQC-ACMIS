from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from Users.models import activity_log
from .models import component_upload_bin, parameter_components #Import the model for data retieving
from .forms import UploadBin_Form, ParameterComponent_Form
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
 

class ParameterIndicatorList(View):
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


def create_uploadBin(request,pk):
    indicator_form = UploadBin_Form(request.POST or None)

    if indicator_form.is_valid():
        indicator_form.instance.parameter_component_id = pk
        indicator_form.instance.created_by = request.user
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

        
        messages.success(request, f'Parameter Upload Bin is successfully created!') 
        return JsonResponse({'status': 'success'}, status=200)
    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': indicator_form.errors}, status=400)
    

@login_required
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


