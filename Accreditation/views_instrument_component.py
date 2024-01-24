import os
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from Users.models import activity_log
from .models import component_upload_bin, parameter_components, uploaded_evidences #Import the model for data retieving
from .forms import FileUpload_Form, ReviewUploadBin_Form, UploadBin_Form, ParameterComponent_Form
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


@login_required
def landing_page(request, pk):
    #Getting the data from the API
    component_form = ParameterComponent_Form(request.POST or None)
    review_form = ReviewUploadBin_Form(request.POST or None)
    uploadBin_form = UploadBin_Form(request.POST or None)
    upload_file_form =  FileUpload_Form(request.POST or None)
    component_records = parameter_components.objects.select_related('area_parameter').filter(area_parameter=pk, is_deleted = False)
    uploaded_records = uploaded_evidences.objects.select_related('upload_bin', 'uploaded_by').filter(is_deleted = False)

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
    
    # print(indicator_details)

    #Getting all the data inside the Program table and storing it to the context variable      
        
    context = { 'component_records': component_records
                , 'component_form': component_form
                , 'uploadBin_form': uploadBin_form
                , 'review_form': review_form
                , 'pk':pk
                , 'indicator_details': indicator_details
                , 'uploaded_records': uploaded_records
                , 'upload_file_form':  upload_file_form
                , 'file_type_mapping': file_type_mapping
                
                }  #Getting all the data inside the type table and storing it to the context variable

    return render(request, 'accreditation-page/instrument-component/main-page/landing-page.html', context)

        
        
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
    return redirect('accreditations:program-accreditation-component', pk=url_pk)

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
    return redirect('accreditations:program-accreditation-component', pk=url_pk)



#------------------------------------------------------------[ ARCHIVE PAGE CODES ]------------------------------------------------------------#
@login_required
def archive_landing(request, pk):
    component_records = parameter_components.objects.select_related('area_parameter').filter(area_parameter=pk)
    review_form = ReviewUploadBin_Form(request.POST or None)

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

    #Getting all the data inside the Program table and storing it to the context variable      
        
    context = { 'component_records': component_records
                , 'pk':pk
                , 'indicator_details': indicator_details
                , 'review_form': review_form
                }  #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-page/instrument-component/archive-page/landing-page.html', context)


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
    return redirect('accreditations:program-accreditation-component-archive', pk=pk)

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
    return redirect('accreditations:program-accreditation-component-archive', pk=pk)


# ---------------------------------- [REVIEW FUNCTIONALITY CODE] -----------------------------#
@login_required
def create_review(request, pk):
# Retrieve the type object with the given primary key (pk)
    try:
        upload_bin = component_upload_bin.objects.get(id=pk)
    except component_upload_bin.DoesNotExist:
        return JsonResponse({'errors': 'Upload Bin not found'}, status=404)

    if request.method == 'POST':
        # Process the form submission with updated data
        review_form = ReviewUploadBin_Form(request.POST or None, instance=upload_bin)
        if review_form.is_valid():
            # Save the updated data to the database
            review_form.instance.modified_by = request.user
            review_form.instance.reviewed_by = request.user
            review_form.instance.reviewed_at = timezone.now()
            review_form.save()  


            # Provide a success message as a JSON response
            messages.success(request, f'Upload Bin is successfully reviewed!') 
            return JsonResponse({'status': 'success'}, status=200)


        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': review_form.errors}, status=400)
        
# ---------------------------------- [ UPLOAD FILE CODES ] -----------------------------#
@login_required
def upload_file(request, pk):
    try:
        upload_bin = component_upload_bin.objects.get(id=pk)
    except component_upload_bin.DoesNotExist:
        return JsonResponse({'errors': 'Upload Bin not found'}, status=404)


    if request.method == 'POST':
        length = request.POST.get('length')

        print('Length value: ',length)
        
        if length != 0:
            upload_bin.status = "ur"
            upload_bin.save()

            if length == upload_bin.accepted_file_count:
                for file_num in range(0, int(length)):
                    print('File:', request.FILES.get(f'files{file_num}'))
                    uploaded_evidences.objects.create(
                        upload_bin_id = pk ,
                        uploaded_by = request.user,
                        file_name =  request.FILES.get(f'files{file_num}'), 
                        file_path=request.FILES.get(f'files{file_num}')
                        
                    )

                messages.success(request, f'Files Uploaded successfully!') 
                return JsonResponse({'status': 'success'}, status=200)
            
            else:
                return JsonResponse({'error': 'Please make sure to submit ' +str(upload_bin.accepted_file_count)+ ' file/s only.'}, status=400)
    
        else:
            return JsonResponse({'error': 'Please attach a file before submitting the form.'}, status=400)
    