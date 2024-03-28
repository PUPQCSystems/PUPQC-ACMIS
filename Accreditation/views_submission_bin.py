from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from Users.models import activity_log
from .models import files, instrument_level, instrument_level_folder #Import the model for data retieving
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
 
def landing_page(request, pk):
    submission_bin_record = instrument_level_folder.objects.get(id=pk)
    parent_pk = ''
    if submission_bin_record.instrument_level:
            parent_pk = submission_bin_record.instrument_level.id

    uploaded_files = files.objects.filter(parent_directory=pk, is_deleted=False)
    # This is for the accepted_file_type mapping. This is for making the file types more presentable
    file_type_mapping = {
        'image/jpeg': 'JPEG',
        'image/png': 'PNG',
        'image/gif': 'GIF',
        'image/bmp': 'BMP',
        'image/svg+xml': 'SVG',
        'image/webp': 'WebP',
        'application/pdf': 'PDF',
        'application/msword': 'Microsoft Word (DOC)',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'Microsoft Word (DOCX)',
        'application/vnd.ms-excel': 'Microsoft Excel (XLS)',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'Microsoft Excel (XLSX)',
        'application/vnd.ms-powerpoint': 'Microsoft PowerPoint (PPT)',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'Microsoft PowerPoint (PPTX)',
        'text/plain': 'Plain Text (TXT)',
        'audio/mp3': 'MP3',
        'video/mp4': 'MP4',
        'audio/ogg': 'Ogg',
        'video/webm': 'WebM',
        'application/zip': 'ZIP',
        'application/x-rar-compressed': 'RAR',
        'text/csv': 'CSV',
        'text/html': 'HTML',
        'text/css': 'CSS',
        'application/javascript': 'JavaScript',
    }

    context = {     'pk':pk
                    , 'submission_bin_record': submission_bin_record
                    , 'file_type_mapping': file_type_mapping
                    , 'uploaded_files': uploaded_files,
                    'parent_pk': parent_pk
                    
                    }  #Getting all the data inside the type table and storing it to the context variable

    return render(request, 'accreditation-submission-bin/main-page/landing-page.html', context)

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
        


def create_files(request, pk):
        try:
            submission_bin = instrument_level_folder.objects.get(id=pk)
        except instrument_level_folder.DoesNotExist:
            return JsonResponse({'errors': 'Submission bin not found'}, status=404)

        if request.method == 'POST':
            length = request.POST.get('length')
            length = int(length)

            if length != 0:
                if length <= submission_bin.accepted_file_count:
                    submission_bin.status = "ur"
                    submission_bin.save()
                    print(submission_bin.accepted_file_count)
                    for file_num in range(0, int(length)):
                        print('File:', request.FILES.get(f'files{file_num}'))
                        files.objects.create(
                            parent_directory_id = pk ,
                            uploaded_by = request.user,
                            file_name =  request.FILES.get(f'files{file_num}'), 
                            file_path=request.FILES.get(f'files{file_num}')
                            
                        )
                    messages.success(request, f'Files Uploaded successfully!') 
                    return JsonResponse({'status': 'success'}, status=200)
                
                else:
                    return JsonResponse({'error': 'Please make sure to submit ' +str(submission_bin.accepted_file_count)+ ' file/s only.'}, status=400)
        
            else:
                return JsonResponse({'error': 'Please attach a file before submitting the form.'}, status=400)


def create_parent_folder_files(request, pk):
    if request.method == 'POST':
        length = request.POST.get('length')
        length = int(length)

        if length != 0:
            for file_num in range(0, int(length)):
                print('File:', request.FILES.get(f'files{file_num}'))
                files.objects.create(
                    instrument_level_id = pk ,
                    uploaded_by = request.user,
                    file_name =  request.FILES.get(f'files{file_num}'), 
                    file_path=request.FILES.get(f'files{file_num}')
                    
                )
            messages.success(request, f'Files Uploaded successfully!') 
            return JsonResponse({'status': 'success'}, status=200)
            
        else:
            return JsonResponse({'error': 'Please attach a file before submitting the form.'}, status=400)
        
def create_child_folder_files(request, pk):
    if request.method == 'POST':
        length = request.POST.get('length')
        length = int(length)

        if length != 0:
            for file_num in range(0, int(length)):
                print('File:', request.FILES.get(f'files{file_num}'))
                files.objects.create(
                    parent_directory_id = pk ,
                    uploaded_by = request.user,
                    file_name =  request.FILES.get(f'files{file_num}'), 
                    file_path=request.FILES.get(f'files{file_num}')
                    
                )
            messages.success(request, f'Files Uploaded successfully!') 
            return JsonResponse({'status': 'success'}, status=200)
            
        else:
            return JsonResponse({'error': 'Please attach a file before submitting the form.'}, status=400)
        
        
@login_required
def archive(request, pk, bin_id):
    # Gets the records who have this ID
    file_record = files.objects.get(id=pk)

    #After getting that record, this code will delete it.
    file_record.modified_by = request.user
    file_record.is_deleted=True
    file_record.deleted_at = timezone.now()
    name = file_record.file_name
    file_record.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "SUBMISSION BIN MODULE"
    activity_log_entry.action = "Archived a File"
    activity_log_entry.type = "ARCHIVE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'The file named "{name}" is successfully archived!') 
    return redirect('accreditations:submission-bin-page', pk=bin_id)



# ------------------------------------------------------------------[ RECYCLE BIN PAGE CODES]------------------------------------------------------------------#

@login_required
def recycle_bin(request, pk):
    uploaded_files = files.objects.filter(is_deleted= True, parent_directory=pk) #Getting all the data inside the Program table and storing it to the context variable

    context =   {   'uploaded_files': uploaded_files,
                    'pk':pk,
                }   #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-submission-bin/recycle-bin/landing-page.html', context)


@login_required
def restore(request, pk):
    # Gets the records who have this ID
    folder_record =  files.objects.get(id=pk)

    #After getting that record, this code will restore it.
    folder_record.modified_by = request.user
    folder_record.deleted_at = None
    folder_record.is_deleted=False
    name = folder_record.file_name
    folder_record.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "RECYCLE BIN MODULE"
    activity_log_entry.action = "Restored a folder"
    activity_log_entry.type = "RESTORE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()


    if folder_record.parent_directory:
        pk = folder_record.parent_directory_id
        messages.success(request, f'The file named {name} is successfully restored!') 
        return redirect('accreditations:submission-bin-recycle-bin-page', pk=pk)

    elif folder_record.instrument_level:
        pk = folder_record.instrument_level_id
        messages.success(request, f'The file named {name} is successfully restored!') 
        return redirect('accreditations:parent-folder-recycle-bin', pk=pk)




@login_required
def destroy(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                file_record =  files.objects.get(id=pk)

                #After getting that record, this code will delete it.
                file_record.delete()

                # Create an instance of the ActivityLog model
                activity_log_entry = activity_log()

                # Set the attributes of the instance
                activity_log_entry.module = "RECYCLE BIN MODULE"
                activity_log_entry.action = "Permanently deleted a File"
                activity_log_entry.type = "DESTROY"
                activity_log_entry.datetime_acted =  timezone.now()
                activity_log_entry.acted_by = request.user
                # Set other attributes as needed

                # Save the instance to the database
                activity_log_entry.save()

                messages.success(request, f'The File is permanently deleted!') 
                return JsonResponse({'success': True, }, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})
