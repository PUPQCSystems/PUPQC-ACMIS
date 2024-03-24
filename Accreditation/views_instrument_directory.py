from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from Users.models import activity_log
from .models import instrument_level_directory #Import the model for data retieving
from .forms import Create_InstrumentDirectory_Form
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
 
@login_required
def landing_page(self, request):
    #Getting the data from the API
    create_form = Create_InstrumentDirectory_Form(request.POST or None)
    records = instrument_level_directory.objects.filter(is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable

    # Initialize an empty list to store update forms for each record
    details = []

    # Iterate through each record and create an update form for it
    for record in records:
        update_form = Create_InstrumentDirectory_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form, created_by, modified_by))
        
    context = { 'records': records, 'create_form': create_form, 'details': details}  #Getting all the data inside the type table and storing it to the context variable

    return render(request, 'accreditation-component/main-page/landing-page.html', context)

@login_required
def create(request):
    create_form = Create_InstrumentDirectory_Form(request.POST or None)

    if create_form.is_valid():
        create_form.instance.created_by = request.user
        create_form.save()
        name = create_form.cleaned_data.get('name')

        # Create an instance of the ActivityLog model
        activity_log_entry = activity_log()

        # Set the attributes of the instance
        activity_log_entry.module = " MODULE"
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
        


