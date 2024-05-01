import os
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, QueryDict
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from Accreditation.forms import PassedResult_Form, RemarksResult_Form, RenameFileForm, RevisitResult_Form
from Accreditation.models import accreditation_certificates, program_accreditation, result_remarks
from django.contrib.auth import authenticate
from datetime import timedelta



@login_required
@permission_required("Accreditation.view_accreditation_certificates", raise_exception=True)
def result_page(request, pk):
    #Getting the data from the API
    passed_result_form = PassedResult_Form(request.POST or None)
    revisit_result_form = RevisitResult_Form(request.POST or None)
    remarks_result_form = RemarksResult_Form(request.POST or None)
    rename_form = RenameFileForm()

    accreditation_record = program_accreditation.objects.get(id=pk)
    certificates_records = accreditation_certificates.objects.select_related('accredited_program').filter( accredited_program_id=pk, is_deleted= False)
    remarks_records = result_remarks.objects.select_related('accredited_program').filter( accredited_program_id=pk).order_by('created_at')
    remarks_counts = result_remarks.objects.filter( accredited_program_id=pk).count()

        
    context = { 
                'passed_result_form': passed_result_form,
                'revisit_result_form': revisit_result_form,
                'records':  certificates_records,
                'accred_program': accreditation_record,
                'remarks_result_form': remarks_result_form,
                'remarks_records':  remarks_records,
                'remarks_counts':  remarks_counts,
                'rename_form': rename_form
               }  #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-page/accreditation-certificates/main-page/landing-page.html', context)



@login_required
@permission_required("Accreditation.accreditation_certificates", raise_exception=True)
def upload_files(request, pk):
    # Retrieve the type object with the given primary key (pk)
    try:
        accreditation_record = program_accreditation.objects.get(id=pk)
    except program_accreditation.DoesNotExist:
        return JsonResponse({'error': 'Program Accreditaion Record not found'}, status=404)


    # update_form = Create_Bodies_Form(instance=type)
    if request.method == 'POST':
        length = request.POST.get('length')
        length = int(length)
        if length != 0:
            for file_num in range(0, int(length)):
                print('File:', request.FILES.get(f'files{file_num}'))
                accreditation_certificates.objects.create(
                    accredited_program_id = pk ,
                    uploaded_by = request.user,
                    certificate_name =  request.FILES.get(f'files{file_num}'), 
                    certificate_path = request.FILES.get(f'files{file_num}')
                    
                ) 
            # Provide a success message as a JSON response
            messages.success(request, f'The File/s are successfully uploaded!') 
            return JsonResponse({"status": "success"}, status=200)
        else:
            return JsonResponse({'error': 'Please attach a file before submitting the form.'}, status=400)
        


    else:
        # Return a validation error as a JSON response
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    

# --------------------------------- [ACCREDITATION RESULT CODES] --------------------------------- #
@login_required
@permission_required("Accreditation.change_program_accreditation", raise_exception=True)
@permission_required("Accreditation.add_program_accreditation", raise_exception=True)
@permission_required("Accreditation.view_program_accreditation", raise_exception=True)
@permission_required("Accreditation.delete_program_accreditation", raise_exception=True)
def result_passed(request, pk):
    # Retrieve the type object with the given primary key (pk)
    try:
        accreditation_record = program_accreditation.objects.get(id=pk)
    except program_accreditation.DoesNotExist:
        return JsonResponse({'errors': 'Program Accreditaion Record not found'}, status=404)

    # Create an instance of the form with the type data
    # update_form = Create_Bodies_Form(instance=type)
    if request.method == 'POST':
        # Process the form submission with updated data
        passed_result_form = PassedResult_Form(request.POST or None, instance=accreditation_record)
        remarks_result_form = RemarksResult_Form(request.POST or None)

        if passed_result_form.is_valid() and remarks_result_form.is_valid():
            remarks_counts = result_remarks.objects.filter( accredited_program_id=pk).count()

            length = request.POST.get('length')
            length = int(length)

            # Get the current datetime in UTC timezone
            entry_result_at = accreditation_record.entry_result_at
            current_datetime = timezone.now()
            passed_result_form.instance.is_done = True
            passed_result_form.instance.is_visited = True
            passed_result_form.instance.entry_result_at = current_datetime
            passed_result_form.instance.status = 'PASSED'
            remarks_result_form.instance.accredited_program = accreditation_record
            remarks_result_form.instance.created_by = request.user

            # Check if the is_failed is True, if true change it to false
            if accreditation_record.is_failed == True:
                passed_result_form.instance.is_failed = False

            # Calculate the time difference
            if entry_result_at:
                time_difference = current_datetime - entry_result_at

                # Check if the time difference is less than or equal to 24 hours and if the date today is less than the revisit date
                if accreditation_record.revisit_date:
                    if time_difference <= timedelta(hours=24) and current_datetime < accreditation_record.revisit_date:
                        passed_result_form.instance.revisit_date = None
                        passed_result_form.instance.revisit_compliance_deadline = None
                        remarks_record = result_remarks.objects.filter(accredited_program_id=pk).order_by('-created_at').first()
                        remarks_record.delete()

                    

            passed_result_form.save()
            if remarks_counts == 2:
                latest_remark = result_remarks.objects.filter(accredited_program_id=pk).latest('created_at')
                latest_remark.remarks =  remarks_result_form.cleaned_data.get('remarks')
                latest_remark.save()
            else:
                remarks_result_form.save()

            if length > 0:
                for file_num in range(0, int(length)):
                    print('File:', request.FILES.get(f'files{file_num}'))
                    accreditation_certificates.objects.create(
                        accredited_program_id = pk ,
                        uploaded_by = request.user,
                        certificate_name =  request.FILES.get(f'files{file_num}'), 
                        certificate_path=request.FILES.get(f'files{file_num}')
                        
                    ) 
            # Provide a success message as a JSON response
            messages.success(request, f'The Accreditation Result is successfully posted!') 
            return JsonResponse({"status": "success"}, status=200)

            


        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': passed_result_form.errors}, status=400)
        

@login_required
@permission_required("Accreditation.change_program_accreditation", raise_exception=True)
@permission_required("Accreditation.add_program_accreditation", raise_exception=True)
@permission_required("Accreditation.view_program_accreditation", raise_exception=True)
@permission_required("Accreditation.delete_program_accreditation", raise_exception=True)
def result_revisit(request, pk):
    # Retrieve the type object with the given primary key (pk)
    try:
        accreditation_record = program_accreditation.objects.get(id=pk)
    except program_accreditation.DoesNotExist:
        return JsonResponse({'errors': 'Program Accreditaion not found'}, status=404)

    # Create an instance of the form with the type data
    # update_form = Create_Bodies_Form(instance=type)
    if request.method == 'POST':
        # Process the form submission with updated data
        revisit_result_form = RevisitResult_Form(request.POST or None, instance=accreditation_record)
        remarks_result_form = RemarksResult_Form(request.POST or None)

        if revisit_result_form.is_valid():
            remarks_counts = result_remarks.objects.filter( accredited_program_id=pk).count()
            entry_result_at = accreditation_record.entry_result_at
            length = request.POST.get('length')
            length = int(length)

            print("LENGTH:", length)

            # Save the updated data to the database
            revisit_result_form.instance.modified_by = request.user
            revisit_result_form.instance.is_done = False
            revisit_result_form.instance.is_failed = False
            revisit_result_form.instance.is_visited = True
            revisit_result_form.instance.validity_date_from = None
            revisit_result_form.instance.validity_date_to = None
            revisit_result_form.instance.status = 'SUBJECT FOR SURVEY REVISIT'
            current_datetime = timezone.now()
            revisit_result_form.instance.entry_result_at = current_datetime
            revisit_result_form.save()

            remarks_result_form.instance.accredited_program = accreditation_record
            remarks_result_form.instance.created_by = request.user

            # Calculate the time difference
            if entry_result_at:
                time_difference = current_datetime - entry_result_at

                if time_difference <= timedelta(hours=24):
                    remarks_record = result_remarks.objects.filter(accredited_program_id=pk).order_by('-created_at').first()
                    remarks_record.delete()

            if remarks_counts == 2:
                latest_remark = result_remarks.objects.filter(accredited_program_id=pk).latest('created_at')
                latest_remark.remarks =  request.POST.get('remarks')
                latest_remark.save()
            else:
                remarks_result_form.save()

            # Saving the files
            if length > 0:
                for file_num in range(0, length):
                    print('File:', request.FILES.get(f'files{file_num}'))
                    accreditation_certificates.objects.create(
                        accredited_program_id = pk ,
                        uploaded_by = request.user,
                        certificate_name =  request.FILES.get(f'files{file_num}'), 
                        certificate_path=request.FILES.get(f'files{file_num}')
                        
                    ) 
            

            # Provide a success message as a JSON response
            messages.success(request, f'The Accreditation Result is successfully posted!') 
            return JsonResponse({"status": "success"}, status=200)

        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': revisit_result_form.errors}, status=400)
        

@login_required
@permission_required("Accreditation.change_program_accreditation", raise_exception=True)
@permission_required("Accreditation.add_program_accreditation", raise_exception=True)
@permission_required("Accreditation.view_program_accreditation", raise_exception=True)
@permission_required("Accreditation.delete_program_accreditation", raise_exception=True)
def result_failed(request, pk):
    # Retrieve the type object with the given primary key (pk)
    try:
        accreditation_record = program_accreditation.objects.get(id=pk)
    except program_accreditation.DoesNotExist:
        return JsonResponse({'errors': 'Program Accreditaion not found'}, status=404)

    # Create an instance of the form with the type data
    # update_form = Create_Bodies_Form(instance=type)
    if request.method == 'POST':
        # Process the form submission with updated data
        remarks_result_form = RemarksResult_Form(request.POST)

        if remarks_result_form.is_valid():
            remarks_counts = result_remarks.objects.filter( accredited_program_id=pk).count()
            length = request.POST.get('length')
            length = int(length)

            print("LENGTH:", length)

            # Save the updated data to the database
            accreditation_record.modified_by = request.user
            accreditation_record.is_failed = True
            accreditation_record.is_done = True
            accreditation_record.status = 'FAILED'
            current_datetime = timezone.now()
            accreditation_record.entry_result_at = current_datetime
            remarks_result_form.instance.accredited_program = accreditation_record
            remarks_result_form.instance.created_by = request.user
            accreditation_record.save()

            if remarks_counts == 2:
                latest_remark = result_remarks.objects.filter(accredited_program_id=pk).latest('created_at')
                latest_remark.remarks =  remarks_result_form.cleaned_data.get('remarks')
                latest_remark.save()
            else:
                remarks_result_form.save()


                            # Saving the files
            if length > 0:
                for file_num in range(0, length):
                    print('File:', request.FILES.get(f'files{file_num}'))
                    accreditation_certificates.objects.create(
                        accredited_program_id = pk ,
                        uploaded_by = request.user,
                        certificate_name =  request.FILES.get(f'files{file_num}'), 
                        certificate_path=request.FILES.get(f'files{file_num}')
                        
                    ) 

            # Provide a success message as a JSON response
            messages.success(request, f'The Accreditation Result is successfully posted!') 
            return JsonResponse({"status": "success"}, status=200)

        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': remarks_result_form.errors}, status=400)
        


# --------------------------------- [ACCREDITATION RESULT CODES] --------------------------------- #

@login_required
@permission_required("Accreditation.delete_accreditation_certificates", raise_exception=True)
def certificate_destroy(request, pk):
    if request.method == 'POST':

        data = QueryDict(request.body.decode('utf-8'))
        entered_password = data.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                accreditation_certificate = accreditation_certificates.objects.get(id=pk)

                #After getting that record, this code will delete it.
                accreditation_certificate.delete()
                messages.success(request, f'The File is permanently deleted!') 
                return JsonResponse({'success': True}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


# FUNCTION IN RENAMING A FILE
@login_required
@permission_required("Accreditation.change_files", raise_exception=True)
def rename_file(request, pk):
    file_obj = get_object_or_404(accreditation_certificates, pk=pk)
    file_name = file_obj.certificate_name
    # Get the extension of the file
    _, extension = os.path.splitext(file_name) 

    if request.method == 'POST':
        form = RenameFileForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data['new_file_name'] + extension


            # Get the records of all accreditation_certificates that have the same parent id
            file_records = accreditation_certificates.objects.filter(accredited_program_id=file_obj.accredited_program_id)
            count = 0
            for file in file_records:
                # Check if there is a file name that is already existing in the database
                if file.certificate_name == new_name:
                    # Increment 1 to count variable if there is already existing in the database
                    count+=1

            if count > 0:
                return JsonResponse({'error': 'File name already exists. Please use a different file name.'}, status=405)

            else:

                file_obj.certificate_name = new_name
                file_obj.modified_by = request.user
                file_obj.certificate_rename_save()
                messages.success(request, f'The File is successfully renamed to {new_name}!')
                return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'errors': 'Invalid request method'}, status=405)
        
