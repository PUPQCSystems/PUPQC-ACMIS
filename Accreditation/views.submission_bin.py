from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from Users.models import activity_log
from .models import instrument_level, instrument_level_folder #Import the model for data retieving
from .forms import Create_InstrumentDirectory_Form
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
 
@login_required
@permission_required("Accreditation.add_component_upload_bin", raise_exception=True)
def create_uploadBin(request,pk):
    submission_bin_form = UploadBin_Form(request.POST or None)


    all_file_types = ['image/jpeg', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                      'application/vnd.ms-excel', 'application/vnd.ms-powerpoint', 'image/png', 'image/gif', 'image/bmp', 'image/svg+xml', 'image/webp', 
                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 
                      'text/plain', 'audio/mp3', 'video/mp4', 'audio/ogg', 'video/webm', 'application/zip', 'application/x-rar-compressed', 'text/csv', 'text/html', 'text/css', 
                      'application/javascript']
    
    if submission_bin_form.is_valid():
        submission_bin_form.instance.parameter_component_id = pk
        submission_bin_form.instance.created_by = request.user
        # submission_bin_form.instance.accepted_file_type = request.POST.getlist('accepted_file_type')
        submission_bin_form.instance.accepted_file_type = all_file_types

        # submission_bin_form.instance.accepted_file_count = request.POST.get('accepted_file_count')
        submission_bin_form.instance.accepted_file_count = 10
        # submission_bin_form.instance.accepted_file_size = request.POST.get('accepted_file_size')
        submission_bin_form.instance.accepted_file_size = 1000
        submission_bin_form.save()

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
        return JsonResponse({'errors': submission_bin_form.errors}, status=400)