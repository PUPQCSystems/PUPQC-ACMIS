import os
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.db.models import Sum

from Users.models import activity_log
from .models import component_upload_bin, instrument_level, instrument_level_area, level_area_parameter, parameter_components, uploaded_evidences #Import the model for data retieving
from .forms import FileUpload_Form, ReviewUploadBin_Form, UploadBin_Form, ParameterComponent_Form
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin


@login_required
@permission_required("Accreditation.view_parameter_components", raise_exception=True)
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
@permission_required("Accreditation.delete_component_upload_bin", raise_exception=True)
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
@permission_required("Accreditation.delete_parameter_components", raise_exception=True)
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
@permission_required("Accreditation.delete_parameter_components", raise_exception=True)
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
@permission_required("Accreditation.delete_parameter_components", raise_exception=True)
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
    return redirect('accreditations:program-accreditation-component-archive-page', pk=pk)

@login_required
@permission_required("Accreditation.delete_component_upload_bin", raise_exception=True)
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
    return redirect('accreditations:program-accreditation-component-archive-page', pk=pk)


# ---------------------------------- [REVIEW FUNCTIONALITY CODE] -----------------------------#
@login_required
@permission_required("Accreditation.change_component_upload_bin", raise_exception=True)
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

            # Get the component record directly using the parameter_component_id
            component_id = upload_bin.parameter_component_id
            component_record = parameter_components.objects.select_related('area_parameter').get(id=component_id)

            # Count all and approved upload bins for the component
            all_upload_bins = component_upload_bin.objects.filter(parameter_component_id=component_id).count()
            approve_upload_bins = component_upload_bin.objects.filter(parameter_component_id=component_id, status="approve").count()

            # Calculate progress for the component
            progress = 0.00
            progress = (approve_upload_bins / all_upload_bins) * 100

            # Update the progress_percentage field of the component record
            component_record.progress_percentage = progress
            component_record.save()

            print("Component Progress:", progress)



            # Get all child parameter_components of the parent area_parameter
            area_parameter_id = component_record.area_parameter_id

            # Get the parameter record
            parameter_record = level_area_parameter.objects.get(id=area_parameter_id)

            # Count all and approved upload bins for all child parameter components of the parameter
            area_parameter_components = parameter_components.objects.filter(area_parameter_id=area_parameter_id)
            all_parameter_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components).count()
            approved_parameter_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components, status="approve").count()

            # Calculate progress for the parameter
            progress = 0.00
            progress = (approved_parameter_bins / all_parameter_bins) * 100

            # Update the progress_percentage field of the parameter record
            parameter_record.progress_percentage = progress
            parameter_record.save()

            print("Parameter Progress:", progress)



# ----------------------------------[ Calculating the progress percentage per each instrument_areas ]--------------------------------------
            
            # Get the area record
            area_record = instrument_level_area.objects.select_related('instrument_level').get(id=parameter_record.instrument_level_area_id)

            # Get all child parameters of the area
            area_parameters = level_area_parameter.objects.filter(instrument_level_area_id=area_record.id)

            # Initialize counters
            all_area_bins = 0
            approved_area_bins = 0

            # Iterate through each parameter
            for parameter in area_parameters:
                # Get all child parameter_components of the parameter
                area_parameter_components = parameter_components.objects.filter(area_parameter_id=parameter.id)

                # Count all and approved bins for each component
                all_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components).count()
                approved_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components, status="approve").count()

                # Increment counters
                all_area_bins += all_bins
                approved_area_bins += approved_bins

            # Calculate progress
            progress = 0.00
            progress = (approved_area_bins / all_area_bins) * 100

            # Update the progress_percentage field of the area record
            area_record.progress_percentage = progress
            area_record.save()

  #----------------[ Codes for calculating program percentage of the program accreditation/ instument_level ]----------------

            instrument_id = area_record.instrument_level.id
            instrument_record = instrument_level.objects.get(id = instrument_id)
            # codes for updateing progress percentage of a specific area   
            # Get the area ID of a specific area from the parameter_component record
            area_records_count = instrument_level_area.objects.filter(instrument_level_id = instrument_id).count()
            overall_percentage = area_records_count * 100
            percentage_sum = instrument_level_area.objects.filter(instrument_level_id=instrument_id).aggregate(Sum('progress_percentage'))['progress_percentage__sum'] or 0
            print("Percentage Sum: ", percentage_sum)
            progress = 0.00
            progress = (percentage_sum / overall_percentage ) * 100
            instrument_record.progress_percentage = progress
            instrument_record.save()

        # Provide a success message as a JSON response
        messages.success(request, f'Upload Bin is successfully reviewed!') 
        return JsonResponse({'status': 'success'}, status=200)

    else:
        # Return a validation error as a JSON response
        return JsonResponse({'errors': review_form.errors}, status=400)
        
# ---------------------------------- [ UPLOAD FILE CODES ] -----------------------------#
@login_required
@permission_required("Accreditation.add_uploaded_evidences", raise_exception=True)
def upload_file(request, pk):
    try:
        upload_bin = component_upload_bin.objects.get(id=pk)
    except component_upload_bin.DoesNotExist:
        return JsonResponse({'errors': 'Upload Bin not found'}, status=404)


    if request.method == 'POST':
        length = request.POST.get('length')
        length = int(length)

        if length != 0:
            if length <= upload_bin.accepted_file_count:
                upload_bin.status = "ur"
                upload_bin.save()
                print(upload_bin.accepted_file_count)
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
        
class FileUpload(PermissionRequiredMixin, View):
    
    permission_required = ["Accreditation.add_uploaded_evidences", "Accreditation.view_uploaded_evidences"]

    def get(self, request, pk, comp_pk):
        upload_bin = component_upload_bin.objects.select_related('parameter_component').get(id=pk, is_deleted = False)
        uploaded_files = uploaded_evidences.objects.select_related('upload_bin').filter(upload_bin_id=upload_bin.id)
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

        context = {     'upload_bin': upload_bin
                        , 'pk':pk
                        , 'comp_pk': comp_pk
                        , 'file_type_mapping': file_type_mapping
                        , 'uploaded_files': uploaded_files
                        
                        }  #Getting all the data inside the type table and storing it to the context variable

        return render(request, 'accreditation-page/instrument-component/main-page/upload-file-page.html', context)
    
    def post(self, request, pk, comp_pk):
        try:
            upload_bin = component_upload_bin.objects.get(id=pk)
        except component_upload_bin.DoesNotExist:
            return JsonResponse({'errors': 'Upload Bin not found'}, status=404)


        if request.method == 'POST':
            length = request.POST.get('length')
            length = int(length)

            if length != 0:
                if length <= upload_bin.accepted_file_count:
                    upload_bin.status = "ur"
                    upload_bin.save()
                    print(upload_bin.accepted_file_count)
                    for file_num in range(0, int(length)):
                        print('File:', request.FILES.get(f'files{file_num}'))
                        uploaded_evidences.objects.create(
                            upload_bin_id = pk ,
                            uploaded_by = request.user,
                            file_name =  request.FILES.get(f'files{file_num}'), 
                            file_path=request.FILES.get(f'files{file_num}')
                            
                        )

                    messages.success(request, f'Files Uploaded successfully!') 
                    redirect_url = f"/accreditation/program-accreditation/area/parameter/upload/{comp_pk}"
                    return JsonResponse({'status': 'success', 'redirect_url': redirect_url}, status=200)
                
                else:
                    return JsonResponse({'error': 'Please make sure to submit ' +str(upload_bin.accepted_file_count)+ ' file/s only.'}, status=400)
        
            else:
                return JsonResponse({'error': 'Please attach a file before submitting the form.'}, status=400)