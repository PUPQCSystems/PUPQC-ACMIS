from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from Users.models import activity_log
from .models import instrument_level, instrument_level_folder #Import the model for data retieving
from .forms import Create_InstrumentDirectory_Form, SubmissionBin_Form
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


all_file_types = ['image/jpeg', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                    'application/vnd.ms-excel', 'application/vnd.ms-powerpoint', 'image/png', 'image/gif', 'image/bmp', 'image/svg+xml', 'image/webp', 
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 
                    'text/plain', 'audio/mp3', 'video/mp4', 'audio/ogg', 'video/webm', 'application/zip', 'application/x-rar-compressed', 'text/csv', 'text/html', 'text/css', 
                    'application/javascript']
 
@login_required
def create_submissionBin_parent(request, pk):
    submission_bin_form = SubmissionBin_Form(request.POST or None)

    if submission_bin_form.is_valid():
        submission_bin_form.instance.instrument_level_id = pk
        submission_bin_form.instance.created_by = request.user
        # submission_bin_form.instance.accepted_file_type = request.POST.getlist('accepted_file_type')
        submission_bin_form.instance.accepted_file_type = all_file_types
        submission_bin_form.instance.is_submission_bin = True

        # submission_bin_form.instance.accepted_file_count = request.POST.get('accepted_file_count')
        submission_bin_form.instance.accepted_file_count = 10
        # submission_bin_form.instance.accepted_file_size = request.POST.get('accepted_file_size')
        submission_bin_form.instance.accepted_file_size = 1000
        submission_bin_form.save()

        # Create an instance of the ActivityLog model
        activity_log_entry = activity_log()

        # Set the attributes of the instance
        activity_log_entry.module = "INSTRUMENT LEVEL FOLDERS MODUL"
        activity_log_entry.action = "Created a Submission Bin"
        activity_log_entry.type = "CREATE"
        activity_log_entry.datetime_acted =  timezone.now()
        activity_log_entry.acted_by = request.user
        # Set other attributes as needed

        # Save the instance to the database
        activity_log_entry.save()

 
        messages.success(request, f'The Submission Bin is successfully created!') 
        return JsonResponse({'status': 'success'}, status=200)
    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': submission_bin_form.errors}, status=400)
    
@login_required
def create_submissionBin_child(request, pk):
    submission_bin_form = SubmissionBin_Form(request.POST or None)
    
    if submission_bin_form.is_valid():
        submission_bin_form.instance.parent_directory_id = pk
        submission_bin_form.instance.created_by = request.user
        # submission_bin_form.instance.accepted_file_type = request.POST.getlist('accepted_file_type')
        submission_bin_form.instance.accepted_file_type = all_file_types
        submission_bin_form.instance.is_submission_bin = True

        # submission_bin_form.instance.accepted_file_count = request.POST.get('accepted_file_count')
        submission_bin_form.instance.accepted_file_count = 10
        # submission_bin_form.instance.accepted_file_size = request.POST.get('accepted_file_size')
        submission_bin_form.instance.accepted_file_size = 1000
        submission_bin_form.save()

        # Create an instance of the ActivityLog model
        activity_log_entry = activity_log()

        # Set the attributes of the instance
        activity_log_entry.module = "INSTRUMENT LEVEL FOLDERS MODUL"
        activity_log_entry.action = "Created a Submission Bin"
        activity_log_entry.type = "CREATE"
        activity_log_entry.datetime_acted =  timezone.now()
        activity_log_entry.acted_by = request.user
        # Set other attributes as needed

        # Save the instance to the database
        activity_log_entry.save()

 
        messages.success(request, f'The Submission Bin is successfully created!') 
        return JsonResponse({'status': 'success'}, status=200)
    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': submission_bin_form.errors}, status=400)
    

@login_required
def update(request, pk):
    # Retrieve the type object with the given primary key (pk)
    try:
        folder_record = instrument_level_folder.objects.get(id=pk)
    except instrument_level_folder.DoesNotExist:
        return JsonResponse({'errors': 'Folder is not found!'}, status=404)

    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = SubmissionBin_Form(request.POST, instance=folder_record)

        if update_form.is_valid():
            # Save the updated data to the database
            update_form.instance.modified_by = request.user
            update_form.instance.accepted_file_type = request.POST.getlist('accepted_file_type')
            update_form.instance.accepted_file_count = request.POST.get('accepted_file_count')
            update_form.instance.accepted_file_size = request.POST.get('accepted_file_size')
            update_form.save()   
            name = update_form.cleaned_data.get('name')

            # Create an instance of the ActivityLog model
            activity_log_entry = activity_log()

            # Set the attributes of the instance
            activity_log_entry.module = "INSTRUMENT LEVEL FOLDERS MODULE"
            activity_log_entry.action = "Modified a Folder"
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
            # Return a validation error using a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)