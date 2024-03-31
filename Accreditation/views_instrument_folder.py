from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from Accreditation.models_views import UserGroupView
from Users.models import activity_log
from .models import accreditation_certificates, files, instrument_level, instrument_level_folder, program_accreditation, user_assigned_to_folder #Import the model for data retieving
from .forms import ChairManAssignedToFolder_Form, CoChairUserAssignedToFolder_Form, Create_InstrumentDirectory_Form, MemberAssignedToFolder_Form, PassedResult_Form, RemarksResult_Form, RevisitResult_Form, SubmissionBin_Form
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
def parent_landing_page(request, pk):
    #Getting the data from the API
    create_form = Create_InstrumentDirectory_Form(request.POST or None)

    chairman_form =ChairManAssignedToFolder_Form(request.POST or None)
    cochairman_form = CoChairUserAssignedToFolder_Form(request.POST or None)
    member_form = MemberAssignedToFolder_Form(request.POST or None)

    passed_result_form = PassedResult_Form(request.POST or None)
    revisit_result_form = RevisitResult_Form(request.POST or None)
    remarks_result_form = RemarksResult_Form(request.POST or None)
    submission_bin_form = SubmissionBin_Form(request.POST or None)
    uploaded_files = files.objects.filter(instrument_level=pk, is_deleted=False)
    certificates_records = accreditation_certificates.objects.select_related('accredited_program').filter(is_deleted= False) 
    records = instrument_level_folder.objects.filter(is_deleted= False, instrument_level=pk, parent_directory= None) #Getting all the data inside the Program table and storing it to the context variable
    instrument_level_record = instrument_level.objects.select_related('instrument').get(id=pk, is_deleted= False)

    try:
        accred_program = program_accreditation.objects.get(instrument_level_id=pk) #Getting all the data inside the Program table and storing it to the context variable
    except ObjectDoesNotExist:
        accred_program = False  # Set accred_program to False when the record does not exist

    user_records = UserGroupView.objects.all()

    # Initialize an empty list to store update forms for each record
    details = []

    # Iterate through each record and create an update form for it
    for record in records:
        update_form = Create_InstrumentDirectory_Form(instance=record)
        assigned_user = user_assigned_to_folder.objects.filter(parent_directory_id=record.id).values_list('assigned_user_id', 'parent_directory_id', 'is_chairman', 'is_cochairman', 'is_member')
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form, created_by, modified_by, assigned_user))

    #Getting all the data inside the type table and storing it to the context variable
    context = { 'records': records, 
                'create_form': create_form, 
                'details': details,
                'instrument_level_record':instrument_level_record,
                'pk': pk,
                'submission_bin_form':submission_bin_form,
                'all_file_types': all_file_types,
                'uploaded_files': uploaded_files,
                'accred_program': accred_program,
                'passed_result_form': passed_result_form,
                'revisit_result_form': revisit_result_form,
                'remarks_result_form': remarks_result_form,
                'certificates_records':  certificates_records,
                'user_records': user_records,
                'chairman_form': chairman_form,
                'cochairman_form': cochairman_form,
                'member_form': member_form,
               }  

    return render(request, 'accreditation-level-parent-directory/main-page/landing-page.html', context)


@login_required
def create(request, pk):
    create_form = Create_InstrumentDirectory_Form(request.POST or None)

    if create_form.is_valid():
        name = create_form.cleaned_data.get('name')
        label = create_form.cleaned_data.get('label')
        due_date = create_form.cleaned_data.get('due_date')
        description = create_form.cleaned_data.get('description')
        has_progress_bar = create_form.cleaned_data.get('has_progress_bar')
        has_assign_button = create_form.cleaned_data.get('has_assign_button')
        can_be_reviewed = create_form.cleaned_data.get('can_be_reviewed')
        create_form.instance.created_by = request.user
        create_form.instance.instrument_level_id = pk
        create_form.instance.is_parent = True
        if label or due_date or description or has_progress_bar or has_assign_button or can_be_reviewed:
            create_form.instance.is_advance = True
        create_form.save()


        # Create an instance of the ActivityLog model
        activity_log_entry = activity_log()

        # Set the attributes of the instance
        activity_log_entry.module = "INSTRUMENT LEVEL FOLDERS MODULE"
        activity_log_entry.action = "Created a Folder"
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
        folder_record = instrument_level_folder.objects.get(id=pk)
    except instrument_level_folder.DoesNotExist:
        return JsonResponse({'errors': 'Folder is not found!'}, status=404)

    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = Create_InstrumentDirectory_Form(request.POST, instance=folder_record)

        if update_form.is_valid():
            name = update_form.cleaned_data.get('name')
            label = update_form.cleaned_data.get('label')
            due_date = update_form.cleaned_data.get('due_date')
            description = update_form.cleaned_data.get('description')
            has_progress_bar = update_form.cleaned_data.get('has_progress_bar')
            has_assign_button = update_form.cleaned_data.get('has_assign_button')
            can_be_reviewed = update_form.cleaned_data.get('can_be_reviewed')
            # Save the updated data to the database
            update_form.instance.modified_by = request.user
            if label or due_date or description or has_progress_bar or has_assign_button or can_be_reviewed :
                update_form.instance.is_advance = True
            update_form.save()  

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
        

@login_required
def archive(request, pk, level_id):
    # Gets the records who have this ID
    folder_record = instrument_level_folder.objects.get(id=pk)

    #After getting that record, this code will delete it.
    folder_record.modified_by = request.user
    folder_record.is_deleted=True
    folder_record.deleted_at = timezone.now()
    name = folder_record.name
    folder_record.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "INSTRUMENT LEVEL FOLDERS MODULE"
    activity_log_entry.action = "Archived a Folder"
    activity_log_entry.type = "ARCHIVE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'The folder named "{name}" is successfully archived!') 
    return redirect('accreditations:instrument-level-directory', pk=level_id)


@login_required
def child_landing_page(request, pk):
    #Getting the data from the API
    create_form = Create_InstrumentDirectory_Form(request.POST or None)
    uploaded_files = files.objects.filter(parent_directory=pk, is_deleted=False)
    records = instrument_level_folder.objects.filter(is_deleted= False, parent_directory=pk) #Getting all the data inside the Program table and storing it to the context variable
    parent_folder = instrument_level_folder.objects.get(is_deleted=False, id=pk) #Getting the data of the parent folder
    # Initialize an empty list to store update forms for each record
    details = []

    # Iterate through each record and create an update form for it
    for record in records:
        update_form = Create_InstrumentDirectory_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form, created_by, modified_by))

    #Getting all the data inside the type table and storing it to the context variable
    context = { 'records': records, 
                'create_form': create_form, 
                'details': details,
                'pk': pk,
                'parent_folder': parent_folder,
                'all_file_types': all_file_types,
                'uploaded_files': uploaded_files,
               }  

    return render(request, 'accreditation-level-child-directory/main-page/landing-page.html', context)


@login_required
def create_child(request, pk):
    create_form = Create_InstrumentDirectory_Form(request.POST or None)

    if create_form.is_valid():
        name = create_form.cleaned_data.get('name')
        label = create_form.cleaned_data.get('label')
        due_date = create_form.cleaned_data.get('due_date')
        description = create_form.cleaned_data.get('description')
        has_progress_bar = create_form.cleaned_data.get('has_progress_bar')
        has_assign_button = create_form.cleaned_data.get('has_assign_button')
        can_be_reviewed = create_form.cleaned_data.get('can_be_reviewed')

        if label or due_date or description or has_progress_bar or has_assign_button or can_be_reviewed:
            create_form.instance.is_advance = True

        create_form.instance.created_by = request.user
        create_form.instance.parent_directory_id = pk
        create_form.save()
        name = create_form.cleaned_data.get('name')

        # Create an instance of the ActivityLog model
        activity_log_entry = activity_log()

        # Set the attributes of the instance
        activity_log_entry.module = "INSTRUMENT LEVEL FOLDERS MODULE"
        activity_log_entry.action = "Created a Folder"
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
def archive_child(request, pk, parent_id):
    # Gets the records who have this ID
    folder_record = instrument_level_folder.objects.get(id=pk)

    #After getting that record, this code will delete it.
    folder_record.modified_by = request.user
    folder_record.is_deleted=True
    folder_record.deleted_at = timezone.now()
    name = folder_record.name
    folder_record.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "INSTRUMENT LEVEL FOLDERS MODULE"
    activity_log_entry.action = "Archived a Folder"
    activity_log_entry.type = "ARCHIVE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'The folder named "{name}" is successfully archived!') 
    return redirect('accreditations:instrument-level-child-directory', pk=parent_id)


# ------------------------------------------------------------------[ RECYCLE BIN PAGE CODES]------------------------------------------------------------------#

@login_required
def parent_recycle_bin(request, pk):
    records = instrument_level_folder.objects.filter(is_deleted= True, instrument_level=pk, parent_directory= None) #Getting all the data inside the Program table and storing it to the context variable
    uploaded_files = files.objects.filter(instrument_level=pk, is_deleted=True)
    instrument_level_record = instrument_level.objects.select_related('instrument').get(id=pk, is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable

    context =   {   'records': records,
                    'instrument_level_record': instrument_level_record,
                    'pk':pk,
                    'uploaded_files': uploaded_files,
                }   #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-level-parent-directory/recycle-bin/landing-page.html', context)

@login_required
def child_recycle_bin(request, pk):
    uploaded_files = files.objects.filter(parent_directory=pk, is_deleted=True)
    records = instrument_level_folder.objects.filter(is_deleted= True, parent_directory=pk) #Getting all the data inside the Program table and storing it to the context variable
    context =   {   'records': records,
                    'pk':pk,
                    'uploaded_files': uploaded_files
                }   #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-level-child-directory/recycle-bin/landing-page.html', context)




@login_required
def restore_parent(request, ins_pk ,pk):
    # Gets the records who have this ID
    folder_record =  instrument_level_folder.objects.get(id=pk)

    #After getting that record, this code will restore it.
    folder_record.modified_by = request.user
    folder_record.deleted_at = None
    folder_record.is_deleted=False
    name = folder_record.name
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

    messages.success(request, f'{name} The Folder is successfully restored!') 
    return redirect('accreditations:parent-folder-recycle-bin', pk=ins_pk)

@login_required
def restore_child(request, parent_pk ,pk):
    # Gets the records who have this ID
    folder_record =  instrument_level_folder.objects.get(id=pk)

    #After getting that record, this code will restore it.
    folder_record.modified_by = request.user
    folder_record.deleted_at = None
    folder_record.is_deleted=False
    name = folder_record.name
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

    messages.success(request, f'{name} The Folder is successfully restored!') 
    return redirect('accreditations:child-folder-recycle-bin', pk=parent_pk)

@login_required
def restore_child_file(request, pk):
    # Gets the records who have this ID
    file_record = files.objects.get(id=pk)

    #After getting that record, this code will restore it.
    file_record.modified_by = request.user
    file_record.deleted_at = None
    file_record.is_deleted=False
    name = file_record.file_name
    file_record.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "RECYCLE BIN MODULE"
    activity_log_entry.action = "Restored a file"
    activity_log_entry.type = "RESTORE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()


    pk = file_record.parent_directory_id
    messages.success(request, f'The file named {name} is successfully restored!') 
    return redirect('accreditations:child-folder-recycle-bin', pk=pk)





@login_required
def destroy(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                folder_record =  instrument_level_folder.objects.get(id=pk)

                #After getting that record, this code will delete it.
                folder_record.delete()

                # Create an instance of the ActivityLog model
                activity_log_entry = activity_log()

                # Set the attributes of the instance
                activity_log_entry.module = "RECYCLE BIN MODULE"
                activity_log_entry.action = "Permanently deleted a Folder"
                activity_log_entry.type = "DESTROY"
                activity_log_entry.datetime_acted =  timezone.now()
                activity_log_entry.acted_by = request.user
                # Set other attributes as needed

                # Save the instance to the database
                activity_log_entry.save()

                messages.success(request, f'The Folder is permanently deleted!') 
                return JsonResponse({'success': True, }, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def archive_files(request, pk):
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

    if file_record.instrument_level:
        messages.success(request, f'The file named "{name}" is successfully archived!') 
        return redirect('accreditations:instrument-level-directory', pk=file_record.instrument_level_id)

    elif file_record.parent_directory:
        messages.success(request, f'The file named "{name}" is successfully archived!') 
        return redirect('accreditations:instrument-level-child-directory', pk=file_record.parent_directory_id)




