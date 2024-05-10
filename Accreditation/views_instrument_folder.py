import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from Accreditation.models_views import UserGroupView
from Accreditation.views_emailing import email_when_file_approved, email_when_file_for_review, email_when_file_request_resubmission, email_when_folder_approved, email_when_folder_for_review, email_when_folder_request_resubmission
from Users.models import activity_log
from .models import accreditation_certificates, files, instrument_level, instrument_level_folder, program_accreditation, user_assigned_to_folder #Import the model for data retieving
from .forms import ChairManAssignedToFolder_Form, CoChairUserAssignedToFolder_Form, Create_InstrumentDirectory_Form, MemberAssignedToFolder_Form, PassedResult_Form, RemarksResult_Form, RenameFileForm, ReviewFile_Form, ReviewUploadBin_Form, RevisitResult_Form, SubmissionBin_Form
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
import ast


all_file_types = ['image/jpeg', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                    'application/vnd.ms-excel', 'application/vnd.ms-powerpoint', 'image/png', 'image/gif', 'image/bmp', 'image/svg+xml', 'image/webp', 
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 
                    'text/plain', 'audio/mp3', 'video/mp4', 'audio/ogg', 'video/webm', 'application/zip', 'application/x-rar-compressed', 'text/csv', 'text/html', 'text/css', 
                    'application/javascript']
@login_required
@permission_required("Accreditation.view_instrument_level_folder", raise_exception=True)
def parent_landing_page(request, pk):
    #Getting the data from the API
    create_form = Create_InstrumentDirectory_Form(request.POST or None)
    rename_form = RenameFileForm()

    chairman_form =ChairManAssignedToFolder_Form(request.POST or None)
    cochairman_form = CoChairUserAssignedToFolder_Form(request.POST or None)
    member_form = MemberAssignedToFolder_Form(request.POST or None)
    review_form = ReviewUploadBin_Form(request.POST or None)

    passed_result_form = PassedResult_Form(request.POST or None)
    revisit_result_form = RevisitResult_Form(request.POST or None)
    remarks_result_form = RemarksResult_Form(request.POST or None)
    submission_bin_form = SubmissionBin_Form(request.POST or None)
    uploaded_files = files.objects.filter(instrument_level=pk, is_deleted=False)
    certificates_records = accreditation_certificates.objects.select_related('accredited_program').filter(is_deleted= False) 
    records = instrument_level_folder.objects.filter(is_deleted= False, instrument_level=pk, parent_directory= None).order_by('name') #Getting all the data inside the Program table and storing it to the context variable
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
        assigned_users = user_assigned_to_folder.objects.select_related('assigned_user').filter(parent_directory_id=record.id)
        assigned_user_ids = user_assigned_to_folder.objects.filter(parent_directory_id=record.id).values_list('assigned_user_id', flat=True)
        users_not_assigned = user_records.exclude(id__in=assigned_user_ids)
        # Convert the string to a Python list
        if record.accepted_file_type:
            converted_file_types = ast.literal_eval(record.accepted_file_type)
        else:
            converted_file_types = None
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form, created_by, modified_by, assigned_users, users_not_assigned, converted_file_types))

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
                'review_form': review_form,
                'rename_form': rename_form
               }  

    return render(request, 'accreditation-level-parent-directory/main-page/landing-page.html', context)


@login_required
@permission_required("Accreditation.add_instrument_level_folder", raise_exception=True)
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

        new_record_id = create_form.instance.id
        folder = instrument_level_folder.objects.select_related('parent_directory', 'instrument_level').get(id=new_record_id)
        if folder.parent_directory_id:
            # Call this function to check if there are existing child records with 'rfr'
            check_status(folder.parent_directory_id)
            calculate_progress(folder.parent_directory_id)

        elif folder.parent_directory_id == None and folder.instrument_level_id:
            parent_calculate_progress(folder.instrument_level_id)

        
        messages.success(request, f'{name} is successfully created!') 
        return JsonResponse({'status': 'success'}, status=200)
    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': create_form.errors}, status=400)
    

@login_required
@permission_required("Accreditation.change_instrument_level_folder", raise_exception=True)
def update(request, pk):
    # Retrieve the type object with the given primary key (pk)
    try:
        folder_record = instrument_level_folder.objects.select_related('parent_directory', 'instrument_level').get(id=pk)
        folder_is_reviewable = folder_record.can_be_reviewed
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


                if can_be_reviewed and folder_is_reviewable == False:
                    update_form.instance.status = 'fr'

                if folder_is_reviewable == True and can_be_reviewed == False:
                    update_form.instance.status = None
                    update_form.instance.remarks = None


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

          
            if folder_record.parent_directory_id:
                # Call this function to check if there are existing child records with 'rfr'
                check_status(folder_record.parent_directory_id)
                calculate_progress(folder_record.parent_directory_id)

            elif folder_record.parent_directory_id == None and folder_record.instrument_level_id:
                parent_calculate_progress(folder_record.instrument_level_id)

            # Provide a success message as a JSON response
            messages.success(request, f'{name} is successfully updated!') 
            return JsonResponse({'status': 'success'}, status=200)

        else:
            # Return a validation error using a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)
        

@login_required
@permission_required("Accreditation.delete_instrument_level_folder", raise_exception=True)
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



    if folder_record.parent_directory_id:
        # Call this function to check if there are existing child records with 'rfr'
        check_status(folder_record.parent_directory_id)
        calculate_progress(folder_record.parent_directory_id)

    elif folder_record.parent_directory_id == None and folder_record.instrument_level_id:
        parent_calculate_progress(folder_record.instrument_level_id)

    messages.success(request, f'The folder named "{name}" is successfully archived!') 
    return redirect('accreditations:instrument-level-directory', pk=level_id)


@login_required
@permission_required("Accreditation.view_instrument_level_folder", raise_exception=True)
def child_landing_page(request, pk):
    def has_folder_access(user, folder):
        # Check if the user is assigned to the given folder
        if user_assigned_to_folder.objects.filter(parent_directory=folder, assigned_user=user).exists():
            return True
        
        # Check if the user is assigned to any parent folders recursively
        parent_folder = folder.parent_directory
        while parent_folder:
            if user_assigned_to_folder.objects.filter(parent_directory=parent_folder, assigned_user=user).exists():
                return True
            parent_folder = parent_folder.parent_directory
        
        return False



    #Getting the data from the API
    create_form = Create_InstrumentDirectory_Form(request.POST or None)
    review_form = ReviewUploadBin_Form(request.POST or None)
    rename_form = RenameFileForm()
    uploaded_files = files.objects.filter(parent_directory=pk, is_deleted=False)
    records = instrument_level_folder.objects.filter(is_deleted= False, parent_directory=pk).order_by('name') #Getting all the data inside the table and storing it to the context variable
    parent_folder = instrument_level_folder.objects.select_related('parent_directory').get(is_deleted=False, id=pk) #Getting the data of the parent folder
    # Initialize an empty list to store update forms for each record
    details = []
    user_records = UserGroupView.objects.all()


    # Check if the logged-in user has access to the parent folder or any of its subfolders
    has_access = has_folder_access(request.user, parent_folder)

    # Check if the user is a chairman of any folder
    is_chairman = user_assigned_to_folder.objects.filter(assigned_user=request.user, is_chairman=True).exists()
    
    for record in records:
        update_form = Create_InstrumentDirectory_Form(instance=record)
        assigned_users = user_assigned_to_folder.objects.select_related('assigned_user').filter(parent_directory_id=record.id)
        assigned_user_ids = user_assigned_to_folder.objects.filter(parent_directory_id=record.id).values_list('assigned_user_id', flat=True)
        users_not_assigned = user_records.exclude(id__in=assigned_user_ids)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        # Convert the string to a Python list
        if record.accepted_file_type:
            converted_file_types = ast.literal_eval(record.accepted_file_type)
        else:
            converted_file_types = None
        details.append((record, update_form, created_by, modified_by, assigned_users, users_not_assigned, converted_file_types))

    #Getting all the data inside the type table and storing it to the context variable
    context = { 'records': records, 
                'create_form': create_form, 
                'details': details,
                'pk': pk,
                'parent_folder': parent_folder,
                'all_file_types': all_file_types,
                'uploaded_files': uploaded_files,
                'has_access': has_access,
                'is_chairman': is_chairman,
                'review_form': review_form,
                'rename_form': rename_form
               }  

    return render(request, 'accreditation-level-child-directory/main-page/landing-page.html', context)


@login_required
@permission_required("Accreditation.add_instrument_level_folder", raise_exception=True)
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

            if can_be_reviewed:
                create_form.instance.status = 'Missing'
                create_form.instance.rating = 0

        create_form.instance.created_by = request.user
        create_form.instance.parent_directory_id = pk
        parent_folder_obj = instrument_level_folder.objects.get(id=pk)

        # Check if the parent folder has instrument_level_id, if so get the id and assign it to child folder
        if parent_folder_obj.instrument_level_id:
            create_form.instance.instrument_level_id = parent_folder_obj.instrument_level_id

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


       # Get the ID of newly created Folder
        new_record_id = create_form.instance.id
        folder = instrument_level_folder.objects.get(id=new_record_id)

        if folder.parent_directory_id:
            # Call this function to check if there are existing child records with 'rfr'
            check_status(folder.parent_directory_id)
            calculate_progress(folder.parent_directory_id)

        elif folder.parent_directory_id == None and folder.instrument_level_id:
            parent_calculate_progress(folder.instrument_level_id)

        
        messages.success(request, f'{name} is successfully created!') 
        return JsonResponse({'status': 'success'}, status=200)
    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': create_form.errors}, status=400)


@login_required
@permission_required("Accreditation.delete_instrument_level_folder", raise_exception=True)
def archive_child(request, pk, parent_id):
    # Gets the records who have this ID
    folder_record = instrument_level_folder.objects.select_related('parent_directory', 'instrument_level').get(id=pk)

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

    if folder_record.parent_directory_id:
        # Call this function to check if there are existing child records with 'rfr'
        check_status(folder_record.parent_directory_id)
        calculate_progress(folder_record.parent_directory_id)

    elif folder_record.parent_directory_id == None and folder_record.instrument_level_id:
        parent_calculate_progress(folder_record.instrument_level_id)


    messages.success(request, f'The folder named "{name}" is successfully archived!') 
    return redirect('accreditations:instrument-level-child-directory', pk=parent_id)


# ------------------------------------------------------------------[ RECYCLE BIN PAGE CODES]------------------------------------------------------------------#

@login_required
@permission_required("Accreditation.delete_instrument_level_folder", raise_exception=True)
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
@permission_required("Accreditation.delete_instrument_level_folder", raise_exception=True)
def child_recycle_bin(request, pk):
    uploaded_files = files.objects.filter(parent_directory=pk, is_deleted=True)
    records = instrument_level_folder.objects.filter(is_deleted= True, parent_directory=pk) #Getting all the data inside the Program table and storing it to the context variable
    context =   {   'records': records,
                    'pk':pk,
                    'uploaded_files': uploaded_files
                }   #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-level-child-directory/recycle-bin/landing-page.html', context)




@login_required
@permission_required("Accreditation.delete_instrument_level_folder", raise_exception=True)
def restore_parent(request, ins_pk ,pk):
    # Gets the records who have this ID
    folder_record =  instrument_level_folder.objects.select_related('parent_directory', 'instrument_level').get(id=pk)

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


    if folder_record.parent_directory_id:
        # Call this function to check if there are existing child records with 'rfr'
        check_status(folder_record.parent_directory_id)
        calculate_progress(folder_record.parent_directory_id)

    elif folder_record.parent_directory_id == None and folder_record.instrument_level_id:
        parent_calculate_progress(folder_record.instrument_level_id)


    messages.success(request, f'{name} The Folder is successfully restored!') 
    return redirect('accreditations:parent-folder-recycle-bin', pk=ins_pk)

@login_required
@permission_required("Accreditation.delete_instrument_level_folder", raise_exception=True)
def restore_child(request, parent_pk ,pk):
    # Gets the records who have this ID
    folder_record =  instrument_level_folder.objects.select_related('parent_directory', 'instrument_level').get(id=pk)

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


    if folder_record.parent_directory_id:
        # Call this function to check if there are existing child records with 'rfr'
        check_status(folder_record.parent_directory_id)
        calculate_progress(folder_record.parent_directory_id)

    elif folder_record.parent_directory_id == None and folder_record.instrument_level_id:
        parent_calculate_progress(folder_record.instrument_level_id)

    messages.success(request, f'The Folder named {name} is successfully restored!') 
    return redirect('accreditations:child-folder-recycle-bin', pk=parent_pk)

@login_required
@permission_required("Accreditation.delete_files", raise_exception=True)
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



    if file_record.parent_directory_id:
        # Call this function to check if there are existing child records with 'rfr'
        check_status(file_record.parent_directory_id)
        calculate_progress(file_record.parent_directory_id)

    elif file_record.parent_directory_id == None and file_record.instrument_level_id:
        parent_calculate_progress(file_record.instrument_level_id)


    messages.success(request, f'The file named {name} is successfully restored!') 
    return redirect('accreditations:child-folder-recycle-bin', pk=file_record.parent_directory_id)





@login_required
@permission_required("Accreditation.delete_instrument_level_folder", raise_exception=True)
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
@permission_required("Accreditation.delete_files", raise_exception=True)
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


    if file_record.parent_directory_id:
        # Call this function to check if there are existing child records with 'rfr'
        check_status(file_record.parent_directory_id)
        calculate_progress(file_record.parent_directory_id)

    elif file_record.parent_directory_id == None and file_record.instrument_level_id:
        parent_calculate_progress(file_record.instrument_level_id)

    if file_record.instrument_level:
        messages.success(request, f'The file named "{name}" is successfully archived!') 
        return redirect('accreditations:instrument-level-directory', pk=file_record.instrument_level_id)

    elif file_record.parent_directory:
        messages.success(request, f'The file named "{name}" is successfully archived!') 
        return redirect('accreditations:instrument-level-child-directory', pk=file_record.parent_directory_id)
    

@login_required
@permission_required("Accreditation.change_instrument_level_folder", raise_exception=True)
def create_folder_review(request, pk):
    try:
        folder = instrument_level_folder.objects.select_related('instrument_level', 'parent_directory').get(id=pk)
    except instrument_level_folder.DoesNotExist:
        try:
            folder = instrument_level_folder.objects.select_related('instrument_level', 'parent_directory').get(instrument_level_id=pk)
        except instrument_level_folder.DoesNotExist:
            return JsonResponse({'errors': 'Folder not found'}, status=404)

    if request.method == 'POST':
        users_assigned_to_folder = user_assigned_to_folder.objects.select_related('assigned_user', 'parent_directory').filter(parent_directory=folder)
        review_form = ReviewUploadBin_Form(request.POST or None, instance=folder)
        review =  request.POST.get('rating')
        remarks=  request.POST.get('remarks')
        if review_form.is_valid():
            review_form.instance.modified_by = request.user
            review_form.instance.reviewed_by = request.user
            review_form.instance.reviewed_at = timezone.now()

            if review == 5:
                review_form.instance.progress_percentage = 100.00
                review_form.instance.rating = review
                review_form.instance.status = "Excellent"

            elif review == 4:
                review_form.instance.progress_percentage = 80.00
                review_form.instance.rating = review
                review_form.instance.status = "Very Satisfactory"


            elif review == 3:
                review_form.instance.progress_percentage = 60.00
                review_form.instance.rating = review
                review_form.instance.status = "Satisfactory"


            elif review == 2:
                review_form.instance.progress_percentage = 40.00
                review_form.instance.rating = review
                review_form.instance.status = "Fair"


            elif review == 1:
                review_form.instance.progress_percentage = 20.00
                review_form.instance.rating = review
                review_form.instance.status = "Poor"

            elif review == 0:
                review_form.instance.progress_percentage = 0.00
                review_form.instance.rating = review
                review_form.instance.status = "Missing"

            #     for user in users_assigned_to_folder:
            #         email_when_folder_approved(folder, user, remarks)

            # elif review == 'rfr':
            #     review_form.instance.progress_percentage = 0.00

            #     for user in users_assigned_to_folder:
            #         email_when_folder_request_resubmission(folder, user, remarks)

            # elif review == 'fr':
            #     review_form.instance.progress_percentage = 0.00

            #     for user in users_assigned_to_folder:
            #         email_when_folder_for_review(folder, user, remarks)


            review_form.save()

            # Call this function to review child records of the parent folder
            review_parent_contents(pk, review)

            if folder.parent_directory_id:
                # Call this function to check if there are existing child records with 'rfr'
                check_status(folder.parent_directory_id)
                calculate_progress(folder.parent_directory_id)

            elif folder.parent_directory_id == None and folder.instrument_level_id:
                parent_calculate_progress(folder.instrument_level_id)
            

            messages.success(request, f'Folder is successfully reviewed!')
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'errors': review_form.errors}, status=400)
    else:
        return JsonResponse({'errors': 'Invalid request method'}, status=405)


def review_parent_contents(parent_folder_id, review):
    try:
        child_folders = instrument_level_folder.objects.filter(Q(has_progress_bar=True) | Q(can_be_reviewed=True), parent_directory_id=parent_folder_id, is_deleted=False)
        child_files = files.objects.filter(can_be_reviewed=True, parent_directory_id=parent_folder_id, is_deleted=False)
    except instrument_level_folder.DoesNotExist:
        return
    

    if child_files:
        for file in child_files:
            file.status = review
            file.save()


    if child_folders:
        for folder in child_folders:
            if folder.has_progress_bar == True or folder.can_be_reviewed == True:
                folder.status = review
                if review == 'rfr':
                    folder.progress_percentage = 0.00
                elif review == 'approve':
                        folder.progress_percentage = 100.00
                folder.save()
    return

def check_status(parent_folder_id):
    # Get the record
    try:
        parent_folder = instrument_level_folder.objects.get(id=parent_folder_id)
    except instrument_level_folder.DoesNotExist:
        return


    # Get the child records of the parent folder with a 'rfr' status
    child_folders_rfr = instrument_level_folder.objects.filter(parent_directory_id=parent_folder_id, status='rfr', is_deleted=False).exists()
    child_files_rfr = files.objects.filter(parent_directory_id=parent_folder_id, status='rfr',  is_deleted=False).exists()

    # Get the child records of the parent folder with a 'fr' status
    child_folders_fr = instrument_level_folder.objects.filter(parent_directory_id=parent_folder_id, status='fr',  is_deleted=False).exists()
    child_files_fr = files.objects.filter(parent_directory_id=parent_folder_id, status='fr', is_deleted=False).exists()

    # Check if there are existing records that have 'rfr' status
    if child_files_rfr or child_folders_rfr:
        # If so, change the status of the parent folder to 'rfr' and save it
        parent_folder.status='rfr'
        parent_folder.save()

    elif child_files_fr or child_folders_fr:
        # If so, change the status of the parent folder to 'fr' and save it
        parent_folder.status='fr'
        parent_folder.save()

    else:
        # Else, change the status of the parent folder to 'approve' and then save it
        parent_folder.status='approve'
        parent_folder.save()

   
    return

@login_required
@permission_required("Accreditation.change_files", raise_exception=True)
def change_to_reviewable_file(request, pk):
    try:
        file_record = files.objects.select_related('parent_directory').get(id=pk)
    except files.DoesNotExist:
        return JsonResponse({'errors': 'File not found'}, status=404)

    if request.method == 'POST':
        file_record.can_be_reviewed = True
        file_record.status = 'fr'
        file_record.modified_by = request.user
        file_record.save()

        if file_record.parent_directory_id:
            # Call this function to check if there are existing child records with 'rfr'
            check_status(file_record.parent_directory_id)
            calculate_progress(file_record.parent_directory_id)

        elif file_record.parent_directory_id == None and file_record.instrument_level_id:
            parent_calculate_progress(file_record.instrument_level_id)


        messages.success(request, f'File is successfully change to reviewable file!')

        if file_record.parent_directory_id == None and file_record.instrument_level_id:
            return redirect('accreditations:instrument-level-directory', pk=file_record.instrument_level_id)
        else:
            return redirect('accreditations:instrument-level-child-directory', pk=file_record.parent_directory_id)

    else:
        return JsonResponse({'errors': 'Invalid request method'}, status=405)

@login_required
@permission_required("Accreditation.change_files", raise_exception=True)
def change_to_not_reviewable_file(request, pk):
    try:
        file_record = files.objects.get(id=pk)
    except files.DoesNotExist:
        return JsonResponse({'errors': 'File not found'}, status=404)

    if request.method == 'POST':
        file_record.can_be_reviewed = False
        file_record.status = None
        file_record.modified_by = request.user
        file_record.save()

        if file_record.parent_directory_id:
            # Call this function to check if there are existing child records with 'rfr'
            check_status(file_record.parent_directory_id)
            calculate_progress(file_record.parent_directory_id)

        elif file_record.parent_directory_id == None and file_record.instrument_level_id:
            parent_calculate_progress(file_record.instrument_level_id)


        messages.success(request, f'File is successfully change to unreviewable file!')
        if file_record.parent_directory_id == None and file_record.instrument_level_id:
            return redirect('accreditations:instrument-level-directory', pk=file_record.instrument_level_id)
        else:
            return redirect('accreditations:instrument-level-child-directory', pk=file_record.parent_directory_id)

    else:
        return JsonResponse({'errors': 'Invalid request method'}, status=405)



@login_required
@permission_required("Accreditation.change_files", raise_exception=True)
def create_file_review(request, pk):
    try:
        file_record = files.objects.select_related('parent_directory','instrument_level', 'uploaded_by').get(id=pk)
    except files.DoesNotExist:
        return JsonResponse({'errors': 'File not found'}, status=404)

    if request.method == 'POST':
        review_form = ReviewFile_Form(request.POST or None, instance=file_record)
        users_assigned_to_folder = user_assigned_to_folder.objects.select_related('assigned_user', 'parent_directory').filter(parent_directory=file_record.parent_directory)
        review =  request.POST.get('rating')
        remarks =  request.POST.get('remarks')
        if review_form.is_valid():
            review_form.instance.modified_by = request.user
            review_form.instance.reviewed_by = request.user
            review_form.instance.reviewed_at = timezone.now()

            if review == '5':
                review_form.instance.rating = review
                review_form.instance.status = "Excellent"

            elif review == '4':
                review_form.instance.rating = review
                review_form.instance.status = "Very Satisfactory"


            elif review == '3':
                review_form.instance.rating = review
                review_form.instance.status = "Satisfactory"


            elif review == '2':
                review_form.instance.rating = review
                review_form.instance.status = "Fair"


            elif review == '1':
                review_form.instance.rating = review
                review_form.instance.status = "Poor"

            elif review == '0':
                review_form.instance.rating = review
                review_form.instance.status = "Missing"

            review_form.save()

            # Call this function to review child records of the parent folder
            review_parent_contents(pk, review)

            if file_record.parent_directory_id:
                # Call this function to check if there are existing child records with 'rfr'
                check_status(file_record.parent_directory_id)
                calculate_progress(file_record.parent_directory_id)

            elif file_record.parent_directory_id == None and file_record.instrument_level_id:
                parent_calculate_progress(file_record.instrument_level_id)



            # if review == 'approve':
            #     review_form.instance.progress_percentage = 100.00

                # if file_record.instrument_level and file_record.parent_directory == None:
                #     email_when_file_approved(file_record, file_record.uploaded_by, remarks)

                # elif file_record.instrument_level and file_record.parent_directory:
                #     email_when_file_approved(file_record, user, remarks)


            # elif review == 'rfr':
            #     review_form.instance.progress_percentage = 0.00

                # for user in users_assigned_to_folder:
                #     email_when_file_request_resubmission(file_record, user, remarks)

            # elif review == 'fr':
            #     review_form.instance.progress_percentage = 0.00

                # for user in users_assigned_to_folder:
                #     email_when_file_for_review(file_record, user, remarks)


            messages.success(request, f'File is successfully reviewed!')
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'errors': review_form.errors}, status=400)
    else:
        return JsonResponse({'errors': 'Invalid request method'}, status=405)





# FUNCTION IN RENAMING A FILE
@login_required
@permission_required("Accreditation.change_files", raise_exception=True)
def rename_file(request, pk):
    file_obj = get_object_or_404(files, pk=pk)
    file_name = file_obj.file_name
    # Get the extension of the file
    _, extension = os.path.splitext(file_name) 

    if request.method == 'POST':
        form = RenameFileForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data['new_file_name'] + extension


            # Get the records of all files that have the same parent id
            file_records = files.objects.filter(parent_directory_id=file_obj.parent_directory_id)
            count = 0
            for file in file_records:
                # Check if there is a file name that is already existing in the database
                if file.file_name == new_name:
                    # Increment 1 to count variable if there is already existing in the database
                    count+=1

            if count > 0:
                return JsonResponse({'error': 'File name already exists. Please use a different file name.'}, status=405)

            else:

                file_obj.file_name = new_name
                file_obj.modified_by = request.user
                file_obj.rename_save()
                messages.success(request, f'The File is successfully renamed to {new_name}!')
                return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'errors': 'Invalid request method'}, status=405)
        



# def parent_calculate_progress(instrument_level_id):
#     # Get the record who has the if of instrument_level_id
#     instrument_level_record = instrument_level.objects.get(id=instrument_level_id)
    
#      # Get the child files and child folders that has a "approved" status
#     folders_count = instrument_level_folder.objects.filter(Q(can_be_reviewed=True) | Q(has_progress_bar=True), instrument_level_id=instrument_level_id, parent_directory_id=None, is_deleted=False).count()
#     files_count = files.objects.filter(can_be_reviewed=True, instrument_level_id=instrument_level_id, parent_directory_id=None, is_deleted=False).count()
#     child_folders = instrument_level_folder.objects.filter(Q(can_be_reviewed=True) | Q(has_progress_bar=True), instrument_level_id=instrument_level_id, parent_directory_id=None, is_deleted=False)
#     child_files = files.objects.filter(can_be_reviewed=True, instrument_level_id=instrument_level_id, parent_directory_id=None, is_deleted=False)
    

#     overall_count = folders_count + files_count
#     overall_percentage = overall_count * 100

#     file_percentage_sum = 0.00
#     folder_percentage_sum = 0.00
#     overall_percentage_sum = 0.00

#     # Get the sum of the progress percentage of all files and folders
#     for folder in child_folders:
#         if folder.has_progress_bar and folder.can_be_reviewed:
#             if folder.progress_percentage:
#                 folder_percentage_sum += float(folder.progress_percentage)

#             else:
#                 folder_percentage_sum += 0.00


#         elif folder.has_progress_bar == True and folder.can_be_reviewed == False:
#             if folder.progress_percentage:
#                 folder_percentage_sum += float(folder.progress_percentage)

#             else:
#                 folder_percentage_sum += 0.00

#         elif folder.has_progress_bar == False and folder.can_be_reviewed:
#             if folder.status == 'approve':
#                 folder_percentage_sum += 100.00
               

#             elif folder.status == 'rfr':
#                 folder_percentage_sum += 0.00
               

#             elif folder.status == "fr":
#                 folder_percentage_sum += 0.00
            

#     for file in child_files:
#         if file.can_be_reviewed:
#             if file.status == 'approve':
#                 file_percentage_sum += 100.00
#             elif file.status == 'rfr':
#                 file_percentage_sum += 0.00

#             elif file.status == "fr":
#                 file_percentage_sum += 0.00

#     overall_percentage_sum = file_percentage_sum + folder_percentage_sum

#     if overall_percentage_sum:
#         progress_percentage = overall_percentage_sum / overall_percentage * 100

#     else:
#         progress_percentage = 0.00
    
#     instrument_level_record.progress_percentage = progress_percentage

#     if progress_percentage == 100.0:
#         instrument_level_record.status = 'approve'

#     else:
#         instrument_level_record.status = 'fr'

#     instrument_level_record.save()
    
#     return


def parent_calculate_progress(instrument_level_id):
    # Get the record who has the if of instrument_level_id
    instrument_level_record = instrument_level.objects.get(id=instrument_level_id)
    
     # Get the child files and child folders that has a "approved" status
    folders_count = instrument_level_folder.objects.filter(Q(can_be_reviewed=True) | Q(has_progress_bar=True), instrument_level_id=instrument_level_id, parent_directory_id=None, is_deleted=False).count()
    files_count = files.objects.filter(can_be_reviewed=True, instrument_level_id=instrument_level_id, parent_directory_id=None, is_deleted=False).count()
    child_folders = instrument_level_folder.objects.filter(Q(can_be_reviewed=True) | Q(has_progress_bar=True), instrument_level_id=instrument_level_id, parent_directory_id=None, is_deleted=False)
    child_files = files.objects.filter(can_be_reviewed=True, instrument_level_id=instrument_level_id, parent_directory_id=None, is_deleted=False)
    

    overall_count = folders_count + files_count
    overall_percentage = overall_count * 100

    folder_rating_sum = 0.00
    file_rating_sum = 0.00
    overall_rating_sum = 0.00
    
    overall_mean = 0.00

    file_percentage_sum = 0.00
    folder_percentage_sum = 0.00
    overall_percentage_sum = 0.00

    
    # Get the sum of the progress percentage of all files and folders
    for folder in child_folders:
        if folder.has_progress_bar and folder.can_be_reviewed:
            if folder.progress_percentage:
                folder_percentage_sum += float(folder.progress_percentage)

            else:
                folder_percentage_sum += 0.00

        elif folder.has_progress_bar == False and folder.can_be_reviewed:

            if folder.rating:
                if float(folder.rating) >= 4.1 and float(folder.rating) <= 5.0:
                    folder_percentage_sum += float(folder.rating) / 5 * 100
                    folder_rating_sum += float(folder.rating)

                elif float(folder.rating) >= 3.1 and float(folder.rating) <= 4.0:
                    folder_percentage_sum += float(folder.rating) / 5 * 100
                    folder_rating_sum += float(folder.rating)
                
                elif float(folder.rating) >= 2.1 and float(folder.rating) <= 3.0:
                    folder_percentage_sum += float(folder.rating) / 5 * 100
                    folder_rating_sum += float(folder.rating)

                elif float(folder.rating) >= 1.1 and float(folder.rating) <= 2.0:
                    folder_percentage_sum += float(folder.rating) / 5 * 100
                    folder_rating_sum += float(folder.rating)

                elif float(folder.rating) >= 0.1 and float(folder.rating) <= 1.0:
                    folder_percentage_sum += float(folder.rating) / 5 * 100
                    folder_rating_sum += float(folder.rating)

                elif float(folder.rating) == 0.0:
                    folder_percentage_sum += float(folder.rating) / 5 * 100
                    folder_rating_sum += float(folder.rating)

    if child_files:
        for file in child_files:
            if file.can_be_reviewed:

                if float(file.rating) >= 4.1 and float(file.rating) <= 5.0:
                    file_percentage_sum += float(file.rating) / 5 * 100
                    file_rating_sum += float(file.rating)

                elif float(file.rating) >= 3.1 and float(file.rating) <= 4.0:
                    file_percentage_sum += float(file.rating) / 5 * 100
                    file_rating_sum += float(file.rating)

                
                elif float(file.rating) >= 2.1 and float(file.rating) <= 3.0:
                    file_percentage_sum += float(file.rating) / 5 * 100
                    file_rating_sum += float(file.rating)

                elif float(file.rating) >= 1.1 and float(file.rating) <= 2.0:
                    file_percentage_sum += float(file.rating) / 5 * 100
                    file_rating_sum += float(file.rating)

                elif float(file.rating) >= 0.1 and float(file.rating) <= 1.0:
                    file_percentage_sum += float(file.rating) / 5 * 100
                    file_rating_sum += float(file.rating)

                elif float(file.rating) == 0.0:
                    file_percentage_sum += float(file.rating) / 5 * 100
                    file_rating_sum += float(file.rating)
    
          
    overall_rating_sum = file_rating_sum + folder_rating_sum
    overall_percentage_sum = file_percentage_sum + folder_percentage_sum

    if overall_percentage_sum:
        progress_percentage = overall_percentage_sum / overall_percentage * 100

    else:
        progress_percentage = 0.00
    instrument_level_record.progress_percentage = progress_percentage

    print('Overall Rating: ', overall_rating_sum)
    if overall_rating_sum:
        mean = overall_rating_sum / overall_count

    else:
        mean = 0
    instrument_level_record.rating = mean
    print('MEAN ', mean)
        

    if progress_percentage >= 81.0 and progress_percentage <= 100.0:
        instrument_level_record.status = 'Excellent'

    elif progress_percentage >= 61.0 and progress_percentage <= 80.0:
        instrument_level_record.status = 'Very Satisfactory'

    elif progress_percentage >= 41.0 and progress_percentage <= 60.0:
        instrument_level_record.status = 'Satisfactory'

    elif progress_percentage >= 21.0 and progress_percentage <= 40.0:
        instrument_level_record.status = 'Fair'

    elif progress_percentage >= 1.0 and progress_percentage <= 20.0:
        instrument_level_record.status = 'Poor'

    elif progress_percentage == 0:
        instrument_level_record.status = 'Missing'


    instrument_level_record.save()

    
    return






def calculate_progress(folder_id):
    folder_record = instrument_level_folder.objects.get(id=folder_id)

    # Get the child files and child folders that has a "approved" status
    folders_count = instrument_level_folder.objects.filter(Q(can_be_reviewed=True) | Q(has_progress_bar=True), parent_directory_id=folder_id, is_deleted=False).count()
    files_count = files.objects.filter(can_be_reviewed=True, parent_directory_id=folder_id, is_deleted=False).count()
    child_folders = instrument_level_folder.objects.filter(Q(can_be_reviewed=True) | Q(has_progress_bar=True), parent_directory_id=folder_id, is_deleted=False)
    child_files = files.objects.filter(can_be_reviewed=True, parent_directory_id=folder_id, is_deleted=False)

    overall_count = folders_count + files_count
    overall_percentage = overall_count * 100

    folder_rating_sum = 0.00
    file_rating_sum = 0.00
    overall_rating_sum = 0.00
    
    overall_mean = 0.00

    file_percentage_sum = 0.00
    folder_percentage_sum = 0.00
    overall_percentage_sum = 0.00

    
    # Get the sum of the progress percentage of all files and folders
    for folder in child_folders:
        if folder.has_progress_bar and folder.can_be_reviewed:
            if folder.progress_percentage:
                folder_percentage_sum += float(folder.progress_percentage)

            else:
                folder_percentage_sum += 0.00

        elif folder.has_progress_bar == False and folder.can_be_reviewed:

            if folder.rating:
                if float(folder.rating) >= 4.1 and float(folder.rating) <= 5.0:
                    folder_percentage_sum += float(folder.rating) / 5 * 100
                    folder_rating_sum += float(folder.rating)

                elif float(folder.rating) >= 3.1 and float(folder.rating) <= 4.0:
                    folder_percentage_sum += float(folder.rating) / 5 * 100
                    folder_rating_sum += float(folder.rating)
                
                elif float(folder.rating) >= 2.1 and float(folder.rating) <= 3.0:
                    folder_percentage_sum += float(folder.rating) / 5 * 100
                    folder_rating_sum += float(folder.rating)

                elif float(folder.rating) >= 1.1 and float(folder.rating) <= 2.0:
                    folder_percentage_sum += float(folder.rating) / 5 * 100
                    folder_rating_sum += float(folder.rating)

                elif float(folder.rating) >= 0.1 and float(folder.rating) <= 1.0:
                    folder_percentage_sum += float(folder.rating) / 5 * 100
                    folder_rating_sum += float(folder.rating)

                elif float(folder.rating) == 0.0:
                    folder_percentage_sum += float(folder.rating) / 5 * 100
                    folder_rating_sum += float(folder.rating)

    if child_files:
        for file in child_files:
            if file.can_be_reviewed:

                if float(file.rating) >= 4.1 and float(file.rating) <= 5.0:
                    file_percentage_sum += float(file.rating) / 5 * 100
                    file_rating_sum += float(file.rating)

                elif float(file.rating) >= 3.1 and float(file.rating) <= 4.0:
                    file_percentage_sum += float(file.rating) / 5 * 100
                    file_rating_sum += float(file.rating)

                
                elif float(file.rating) >= 2.1 and float(file.rating) <= 3.0:
                    file_percentage_sum += float(file.rating) / 5 * 100
                    file_rating_sum += float(file.rating)

                elif float(file.rating) >= 1.1 and float(file.rating) <= 2.0:
                    file_percentage_sum += float(file.rating) / 5 * 100
                    file_rating_sum += float(file.rating)

                elif float(file.rating) >= 0.1 and float(file.rating) <= 1.0:
                    file_percentage_sum += float(file.rating) / 5 * 100
                    file_rating_sum += float(file.rating)

                elif float(file.rating) == 0.0:
                    file_percentage_sum += float(file.rating) / 5 * 100
                    file_rating_sum += float(file.rating)
    
          
    overall_rating_sum = file_rating_sum + folder_rating_sum
    overall_percentage_sum = file_percentage_sum + folder_percentage_sum

    if overall_percentage_sum:
        progress_percentage = overall_percentage_sum / overall_percentage * 100

    else:
        progress_percentage = 0.00
    folder_record.progress_percentage = progress_percentage

    print('Overall Rating: ', overall_rating_sum)
    if overall_rating_sum:
        mean = overall_rating_sum / overall_count

    else:
        mean = 0
    folder_record.rating = mean
    print(folder_record.name, ': ', mean)
        

    if progress_percentage >= 81.0 and progress_percentage <= 100.0:
        folder_record.status = 'Excellent'

    elif progress_percentage >= 61.0 and progress_percentage <= 80.0:
        folder_record.status = 'Very Satisfactory'

    elif progress_percentage >= 41.0 and progress_percentage <= 60.0:
        folder_record.status = 'Satisfactory'

    elif progress_percentage >= 21.0 and progress_percentage <= 40.0:
        folder_record.status = 'Fair'

    elif progress_percentage >= 1.0 and progress_percentage <= 20.0:
        folder_record.status = 'Poor'

    elif progress_percentage == 0:
        folder_record.status = 'Missing'


    folder_record.save()

    if folder_record.parent_directory_id:
        calculate_progress(folder_record.parent_directory_id)

    elif folder_record.parent_directory_id == None and folder_record.instrument_level_id:
        parent_calculate_progress(folder_record.instrument_level_id)
    
    return



