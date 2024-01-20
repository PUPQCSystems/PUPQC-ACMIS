from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from Users.models import activity_log
from .models import parameter #Import the model for data retieving
from .forms import Parameter_Form
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
 

class ParameterList(View):
    def get(self, request):
        #Getting the data from the API
        create_form = Parameter_Form(request.POST or None)
        records = parameter.objects.filter(is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable

        # Initialize an empty list to store update forms for each record
        details = []

        # Iterate through each record and create an update form for it
        for record in records:
            update_form = Parameter_Form(instance=record)
            created_by = record.created_by  # Get the user who created the record
            modified_by = record.modified_by  # Get the user who modified the record
            details.append((record, update_form, created_by, modified_by))
            
        context = { 'records': records, 'create_form': create_form, 'details': details}  #Getting all the data inside the type table and storing it to the context variable

        return render(request, 'accreditation-parameter/main-page/landing-page.html', context)

    
    def post(self, request):
        create_form = Parameter_Form(request.POST or None)

        if create_form.is_valid():
            create_form.instance.created_by = request.user
            create_form.save()
            name = create_form.cleaned_data.get('name')

            # Create an instance of the ActivityLog model
            activity_log_entry = activity_log()

            # Set the attributes of the instance
            activity_log_entry.module = "ACCREDITATION PARAMETER MODULE"
            activity_log_entry.action = "Created a record"
            activity_log_entry.type = "CREATE"
            activity_log_entry.datetime_acted =  timezone.now()
            activity_log_entry.acted_by = request.user
            # Set other attributes as needed

            # Save the instance to the database
            activity_log_entry.save()

            messages.success(request, f'{name} is successfully created!') 
            return JsonResponse({'status': 'success'}, status=200)
        else:
            # Return a validation error using a JSON response
            return JsonResponse({'errors': create_form.errors}, status=400)
        
   
@login_required
def update(request, pk):
# Retrieve the type object with the given primary key (pk)
    try:
        parameter_record = parameter.objects.get(id=pk)
    except parameter.DoesNotExist:
        return JsonResponse({'errors': 'parameter not found'}, status=404)

    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = Parameter_Form(request.POST or None, instance=parameter_record)
        if update_form.is_valid():
            # Save the updated data to the database
            update_form.instance.modified_by = request.user
            update_form.save()  
            name = update_form.cleaned_data.get('name')

            # Create an instance of the ActivityLog model
            activity_log_entry = activity_log()

            # Set the attributes of the instance
            activity_log_entry.module = "ACCREDITATION PARAMETER MODULE"
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
        
@login_required
def archive(request, pk):
    # Gets the records who have this ID
    parameter_record = parameter.objects.get(id=pk)

    #After getting that record, this code will delete it.
    parameter_record.modified_by = request.user
    parameter_record.is_deleted=True
    parameter_record.deleted_at = timezone.now()
    name = parameter_record.name
    parameter_record.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "ACCREDITATION PARAMETER MODULE"
    activity_log_entry.action = "Archived a record"
    activity_log_entry.type = "ARCHIVE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'{name} is successfully archived!') 
    return redirect('accreditations:parameter-landing')



#------------------------------------------------------------[ ARCHIVE PAGE CODES ]------------------------------------------------------------#
@login_required
def archive_landing(request):
    records = parameter.objects.filter(is_deleted= True) #Getting all th

    details = []
     # Iterate through each record and create an update form for it
    for record in records:
        update_form = Parameter_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form,created_by, modified_by))

    context = { 'details': details, 'records': records }#Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-parameter/archive-page/landing-page.html', context)


@login_required
def restore(request, pk):
    # Gets the records who have this ID
    parameter_record =  parameter.objects.get(id=pk)

    #After getting that record, this code will restore it.
    parameter_record.modified_by = request.user
    parameter_record.deleted_at = None
    parameter_record.is_deleted=False
    name = parameter_record.name
    parameter_record.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "ACCREDITATION PARAMETER MODULE"
    activity_log_entry.action = "Restored a record"
    activity_log_entry.type = "RESTORE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'{name} parameter is successfully restored!') 
    return redirect('accreditations:parameter-archive-page')


@login_required
def destroy(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                parameter_record =  parameter.objects.get(id=pk)

                #After getting that record, this code will delete it.
                parameter_record.delete()

                # Create an instance of the ActivityLog model
                activity_log_entry = activity_log()

                # Set the attributes of the instance
                activity_log_entry.module = "ACCREDITATION PARAMETER MODULE"
                activity_log_entry.action = "Permanently deleted a record"
                activity_log_entry.type = "DESTROY"
                activity_log_entry.datetime_acted =  timezone.now()
                activity_log_entry.acted_by = request.user
                # Set other attributes as needed

                # Save the instance to the database
                activity_log_entry.save()

                messages.success(request, f'Parameter is permanently deleted!') 
                url_landing = "/accreditation/parameter/archive-page/"
                return JsonResponse({'success': True, 'url_landing': url_landing}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


