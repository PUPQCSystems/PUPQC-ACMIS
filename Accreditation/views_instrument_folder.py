from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from Accreditation.models_views import UserGroupView
from Users.models import activity_log
from .models import accreditation_certificates, files, instrument_level, instrument_level_folder, program_accreditation, user_assigned_to_folder #Import the model for data retieving
from .forms import ChairManAssignedToFolder_Form, CoChairUserAssignedToFolder_Form, Create_InstrumentDirectory_Form, MemberAssignedToFolder_Form, PassedResult_Form, RemarksResult_Form, ReviewFile_Form, ReviewUploadBin_Form, RevisitResult_Form, SubmissionBin_Form
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import ast

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
    review_form = ReviewUploadBin_Form(request.POST or None)

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
                'review_form': review_form
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

        new_record_id = create_form.instance.id
        new_folder_obj = instrument_level_folder.objects.select_related('parent_directory', 'instrument_level').get(id=new_record_id)
        update_progress(new_folder_obj)

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
        folder_record = instrument_level_folder.objects.select_related('parent_directory', 'instrument_level').get(id=pk)
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

                if can_be_reviewed:
                    update_form.instance.status = 'fr'

            update_form.save()  

            update_progress(folder_record)

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


    update_progress(folder_record)

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
    uploaded_files = files.objects.filter(parent_directory=pk, is_deleted=False)
    records = instrument_level_folder.objects.filter(is_deleted= False, parent_directory=pk) #Getting all the data inside the table and storing it to the context variable
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
                'review_form': review_form
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

            if can_be_reviewed:
                create_form.instance.status = 'fr'

        create_form.instance.created_by = request.user
        create_form.instance.parent_directory_id = pk
        parent_folder_obj = instrument_level_folder.objects.get(id=pk)

        # Check if the parent folder has instrument_level_id, if so get the id and assign it to child folder
        if parent_folder_obj.instrument_level_id:
            create_form.instance.instrument_level_id = parent_folder_obj.instrument_level_id

        create_form.save()

        # Get the ID of newly created Folder
        new_record_id = create_form.instance.id
        new_folder_obj = instrument_level_folder.objects.select_related('parent_directory', 'instrument_level').get(id=new_record_id)
        update_progress(new_folder_obj)

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
    folder_record = instrument_level_folder.objects.select_related('parent_directory', 'instrument_level').get(id=pk)

    #After getting that record, this code will delete it.
    folder_record.modified_by = request.user
    folder_record.is_deleted=True
    folder_record.deleted_at = timezone.now()
    name = folder_record.name
    folder_record.save()

    update_progress(folder_record)
    
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
    folder_record =  instrument_level_folder.objects.select_related('parent_directory', 'instrument_level').get(id=pk)

    #After getting that record, this code will restore it.
    folder_record.modified_by = request.user
    folder_record.deleted_at = None
    folder_record.is_deleted=False
    name = folder_record.name
    folder_record.save()
    update_progress(folder_record)


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
    folder_record =  instrument_level_folder.objects.select_related('parent_directory', 'instrument_level').get(id=pk)

    #After getting that record, this code will restore it.
    folder_record.modified_by = request.user
    folder_record.deleted_at = None
    folder_record.is_deleted=False
    name = folder_record.name

    update_progress(folder_record)
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
    


def calculate_progress(folder):
    # Get all child subfolders of the current folder
    # Retrieve subfolders with either "has_progress_bar" or "can_be_reviewed" set to true
    child_subfolders = instrument_level_folder.objects.select_related('parent_directory', 'instrument_level').filter(Q(has_progress_bar=True) | Q(can_be_reviewed=True), parent_directory=folder, is_deleted=False)

    # Initialize counters for all and approved bins
    all_bins = 0
    approved_bins = 0

    # Iterate through each child subfolder
    for subfolder in child_subfolders:
        # If the child subfolder has children, recursively calculate progress
        if subfolder.is_parent:
            child_progress = calculate_progress(subfolder)
            all_bins += child_progress['all']
            approved_bins += child_progress['approved']
            
        else:
            # Count all and approved bins for the child subfolder
            all_bins += 1
            if subfolder.status == "approve":
                approved_bins += 1
                    
    return {'all': all_bins, 'approved': approved_bins}

def update_progress(folder):
    # Calculate progress for the folder
    progress_data = calculate_progress(folder)
    all_bins = progress_data['all']
    approved_bins = progress_data['approved']
    progress_percentage = (approved_bins / all_bins) * 100 if all_bins > 0 else 0

    # Update progress percentage for the folder
    folder.progress_percentage = progress_percentage
    folder.save()

    # Recursively update progress for parent subfolder
    if folder.parent_directory and folder.instrument_level:
        parent_folder = instrument_level_folder.objects.select_related('parent_directory', 'instrument_level').get(id=folder.parent_directory_id, is_deleted=False)
        update_progress(parent_folder)

    elif folder.instrument_level and folder.parent_directory == None:
        update_instrument_level_progress(folder.instrument_level_id)

# Update progress for the instrument level folder
def update_instrument_level_progress(instrument_level_id):

    instrument_level_obj = instrument_level.objects.get(id=instrument_level_id)

    # Count the number of approved subfolders for the instrument_level
    subfolders = instrument_level_folder.objects.select_related('instrument_level').filter(instrument_level_id=instrument_level_id, has_progress_bar=True, is_deleted=False)

    progress = 0.00
    progress_percentage_result=0.00
    overall_progress=0.00
    count = 0
    for record in subfolders:
        if record.progress_percentage:
            progress += float(record.progress_percentage)
        count+=1
	
    overall_progress = 100 * count
    if progress and overall_progress:
        progress_percentage_result= (progress / overall_progress) * 100
        progress_percentage_result = round(progress_percentage_result, 2)

    # Update progress percentage for the instrument_level
    print('progress_percentage_result: ', progress_percentage_result)
    instrument_level_obj.progress_percentage = progress_percentage_result
    instrument_level_obj.save()

@login_required
def create_folder_review(request, pk):
    try:
        subfolder = instrument_level_folder.objects.select_related('instrument_level', 'parent_directory').get(id=pk)
    except instrument_level_folder.DoesNotExist:
        return JsonResponse({'errors': 'Folder not found'}, status=404)

    if request.method == 'POST':
        review_form = ReviewUploadBin_Form(request.POST or None, instance=subfolder)
        if review_form.is_valid():
            review_form.instance.modified_by = request.user
            review_form.instance.reviewed_by = request.user
            review_form.instance.reviewed_at = timezone.now()
            review_form.save()

            # Update progress percentage for the current folder and its parent subfolder recursively
            update_progress(subfolder)

            messages.success(request, f'Folder is successfully reviewed!')
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'errors': review_form.errors}, status=400)
    else:
        return JsonResponse({'errors': 'Invalid request method'}, status=405)



@login_required
def create_file_review(request, pk):
    try:
        file_record = files.objects.select_related('parent_directory').get(id=pk)
    except instrument_level_folder.DoesNotExist:
        return JsonResponse({'errors': 'File not found'}, status=404)

    if request.method == 'POST':
        review_form = ReviewFile_Form(request.POST or None, instance=file_record)
        if review_form.is_valid():
            review_form.instance.modified_by = request.user
            review_form.instance.reviewed_by = request.user
            review_form.instance.reviewed_at = timezone.now()
            review_form.save()

            messages.success(request, f'File is successfully reviewed!')
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'errors': review_form.errors}, status=400)
    else:
        return JsonResponse({'errors': 'Invalid request method'}, status=405)
