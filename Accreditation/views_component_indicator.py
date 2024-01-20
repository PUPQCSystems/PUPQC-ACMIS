from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from Users.models import activity_log
from .models import parameter_component_indicators, parameter_components #Import the model for data retieving
from .forms import ComponentIndicator_Form, ParameterComponent_Form
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
 

class ParameterIndicatorList(View):
    def get(self, request, pk):
        #Getting the data from the API
        component_form = ParameterComponent_Form(request.POST or None)
        indicator_form = ComponentIndicator_Form(request.POST or None)
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

            indicator_records = parameter_component_indicators.objects.select_related('parameter_component').filter(parameter_component=component_record.id, is_deleted = False)
            if indicator_records:
                for indicator_record in  indicator_records.values():
                    # Convert the dictionary back to a model instance
                    indicator_instance = parameter_component_indicators(**indicator_record)
                    
                    # Now you can use the instance with the form
                    indicator_update_form = ComponentIndicator_Form(instance=indicator_instance)
                    indicator_record['indicator_update_form'] = indicator_update_form
                    records.append(indicator_record)
            
            indicator_details[component_record] = records
        
        print(indicator_details)

        #Getting all the data inside the Program table and storing it to the context variable      
            
        context = { 'component_records': component_records
                   , 'component_form': component_form
                   , 'indicator_form': indicator_form
                   , 'pk':pk
                   , 'indicator_details': indicator_details
                   
                   }  #Getting all the data inside the type table and storing it to the context variable

        return render(request, 'accreditation-parameter-indicator/main-page/landing-page.html', context)

    
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
            activity_log_entry.module = "PARAMETER INDICATOR MODULE"
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


def create_indicator(request,pk):
    indicator_form = ComponentIndicator_Form(request.POST or None)

    if indicator_form.is_valid():
        indicator_form.instance.parameter_component_id = pk
        indicator_form.instance.created_by = request.user
        indicator_form.save()

        # Create an instance of the ActivityLog model
        activity_log_entry = activity_log()

        # Set the attributes of the instance
        activity_log_entry.module = "PARAMETER INDICATOR MODULE"
        activity_log_entry.action = "Created a record"
        activity_log_entry.type = "CREATE"
        activity_log_entry.datetime_acted =  timezone.now()
        activity_log_entry.acted_by = request.user
        # Set other attributes as needed

        # Save the instance to the database
        activity_log_entry.save()

        
        messages.success(request, f'Indicator is successfully created!') 
        return JsonResponse({'status': 'success'}, status=200)
    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': indicator_form.errors}, status=400)
    
def create_subindicator(request,comp_pk, ind_pk):
    indicator_form = ComponentIndicator_Form(request.POST or None)

    if indicator_form.is_valid():
        indicator_form.instance.parameter_component_id = comp_pk
        indicator_form.instance.sub_indicator_id = ind_pk
        indicator_form.instance.created_by = request.user
        indicator_form.save()

        # Create an instance of the ActivityLog model
        activity_log_entry = activity_log()

        # Set the attributes of the instance
        activity_log_entry.module = "PARAMETER INDICATOR MODULE"
        activity_log_entry.action = "Created a record"
        activity_log_entry.type = "CREATE"
        activity_log_entry.datetime_acted =  timezone.now()
        activity_log_entry.acted_by = request.user
        # Set other attributes as needed

        # Save the instance to the database
        activity_log_entry.save()

        
        messages.success(request, f' Indicator is successfully created!') 
        return JsonResponse({'status': 'success'}, status=200)
    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': indicator_form.errors}, status=400)

@login_required
def update_indicator(request, pk):
# Retrieve the type object with the given primary key (pk)
    try:
        indicator_record = parameter_component_indicators.objects.get(id=pk)
    except parameter_component_indicators.DoesNotExist:
        return JsonResponse({'errors': 'Indicator not found'}, status=404)

    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = ComponentIndicator_Form(request.POST or None, instance=indicator_record)
        if update_form.is_valid():
            # Save the updated data to the database
            update_form.instance.modified_by = request.user
            update_form.save()  

            # Create an instance of the ActivityLog model
            activity_log_entry = activity_log()

            # Set the attributes of the instance
            activity_log_entry.module = "PARAMETER INDICATOR MODULE"
            activity_log_entry.action = "Modified a record"
            activity_log_entry.type = "UPDATE"
            activity_log_entry.datetime_acted =  timezone.now()
            activity_log_entry.acted_by = request.user
            # Set other attributes as needed

            # Save the instance to the database
            activity_log_entry.save()

            # Provide a success message as a JSON response
            messages.success(request, f'Indicator is successfully updated!') 
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
            activity_log_entry.module = "PARAMETER INDICATOR MODULE"
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
def archive_indicator(request, url_pk, record_pk):
    # Gets the records who have this ID
    indicator_record = parameter_component_indicators.objects.get(id=record_pk)

    #After getting that record, this code will delete it.
    indicator_record.modified_by = request.user
    indicator_record.is_deleted=True
    indicator_record.deleted_at = timezone.now()
    indicator_record.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "PARAMETER INDICATOR MODULE"
    activity_log_entry.action = "Archived a record"
    activity_log_entry.type = "ARCHIVE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'Indicator is successfully archived!') 
    return redirect('accreditations:instrument-parameter-indicator', pk=url_pk)

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
    activity_log_entry.module = "PARAMETER INDICATOR MODULE"
    activity_log_entry.action = "Archived a record"
    activity_log_entry.type = "ARCHIVE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'Component is successfully archived!') 
    return redirect('accreditations:instrument-parameter-indicator', pk=url_pk)



#------------------------------------------------------------[ ARCHIVE PAGE CODES ]------------------------------------------------------------#
@login_required
def archive_landing(request):
    records = parameter_components.objects.filter(is_deleted= True) #Getting all th

    details = []
     # Iterate through each record and create an update form for it
    for record in records:
        update_form = ParameterComponent_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form,created_by, modified_by))

    context = { 'details': details, 'records': records }#Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-parameter-component/archive-page/landing-page.html', context)


@login_required
def restore(request, pk):
    # Gets the records who have this ID
    component_record =  parameter_components.objects.get(id=pk)

    #After getting that record, this code will restore it.
    component_record.modified_by = request.user
    component_record.deleted_at = None
    component_record.is_deleted=False
    name = component_record.name
    component_record.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "PARAMETER INDICATOR MODULE"
    activity_log_entry.action = "Restored a record"
    activity_log_entry.type = "RESTORE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'{name} parameter is successfully restored!') 
    return redirect('accreditations:instrument-parameter-indicator-archive-page')


@login_required
def destroy(request, pk):
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
                activity_log_entry.module = "PARAMETER INDICATOR MODULE"
                activity_log_entry.action = "Permanently deleted a record"
                activity_log_entry.type = "DESTROY"
                activity_log_entry.datetime_acted =  timezone.now()
                activity_log_entry.acted_by = request.user
                # Set other attributes as needed

                # Save the instance to the database
                activity_log_entry.save()

                messages.success(request, f'Parameter is permanently deleted!') 
                return JsonResponse({'success': True}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


