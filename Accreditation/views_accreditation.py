from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from Accreditation.forms import FailedResult_Form, PassedResult_Form, ProgramAccreditation_Form, ProgramAccreditation_UpdateForm, RevisitResult_Form
from Accreditation.models import accreditation_certificates, instrument, instrument_level, program_accreditation
from django.core.serializers import serialize
from django.contrib.auth import authenticate
from datetime import timedelta


# Create your views here.

@login_required
@permission_required("Accreditation.view_program_accreditation", raise_exception=True)
def landing_page(request):
    #Getting the data from the API
    passed_result_form = PassedResult_Form(request.POST or None)
    revisit_result_form = RevisitResult_Form(request.POST or None)
    failed_result_form = FailedResult_Form(request.POST or None)
    create_form = ProgramAccreditation_Form(request.POST or None)

    certificates_records = accreditation_certificates.objects.select_related('accredited_program').filter(is_deleted= False) 
    records = program_accreditation.objects.select_related('instrument_level', 'program').filter(is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable

    # Initialize an empty list to store update forms for each record
    details = []

    # Iterate through each record and create an update form for it
    for record in records:
        update_form = ProgramAccreditation_UpdateForm(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form, created_by, modified_by))
        
    context = { 'records': records, 
               'create_form': create_form, 
               'details': details,
               'passed_result_form': passed_result_form,
               'failed_result_form': failed_result_form,
               'revisit_result_form': revisit_result_form,
               'certificates_records':  certificates_records 
               }  #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-page/program-accreditation/main-page/landing-page.html', context)

@login_required
@permission_required("Accreditation.add_program_accreditation", raise_exception=True)
def create(request):
    create_form = ProgramAccreditation_Form(request.POST or None)
    if create_form.is_valid():
        create_form.instance.created_by = request.user
        create_form.save()
        program = create_form.cleaned_data.get('program')
        messages.success(request, f'{program} is now ready for accreditation!') 
        return JsonResponse({'success': True }, status=200)

    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': create_form.errors}, status=400)
    
def filter_instrument(request):
    program_id = request.GET.get('program_id')

    # Check if program_id is provided and is a valid integer
    if not program_id:
        return JsonResponse({'errors': 'Please select a valid option'}, status=400)
    else:
        # Check if there are instrument records for the provided program_id
        instrument_records = instrument.objects.filter(program=program_id, is_deleted=False)

        if not instrument_records.exists():
            return JsonResponse({'errors': 'No instruments found for the provided program'}, status=404)


        for instrument_record in instrument_records:
            instrument_id = instrument_record.id       
        instrument_levels = instrument_level.objects.filter(instrument_id =instrument_id, is_deleted=False)

        options = {}
        for choices_level in instrument_levels:
                option = choices_level.level.name +' - '+choices_level.instrument.name
                options[choices_level.id] = option

        return JsonResponse({'instrument_levels': options})

@login_required
@permission_required("Accreditation.change_program_accreditation", raise_exception=True)
def update(request, pk):
    # Retrieve the type object with the given primary key (pk)
    try:
        accreditation_record = program_accreditation.objects.get(id=pk)
    except program_accreditation.DoesNotExist:
        return JsonResponse({'errors': 'Program Accreditaion not found'}, status=404)

    # Create an instance of the form with the type data
    # update_form = Create_Bodies_Form(instance=type)
    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = ProgramAccreditation_UpdateForm(request.POST or None, instance=accreditation_record)
        if update_form.is_valid():
            # Save the updated data to the database
            update_form.instance.modified_by = request.user
            update_form.save()
            program = update_form.cleaned_data.get('program')

            # Provide a success message as a JSON response
            messages.success(request, f'{program} is successfully updated!') 

            return JsonResponse({"status": "success"}, status=200)

        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)
 
 
@login_required
@permission_required("Accreditation.delete_program_accreditation", raise_exception=True)
def archive(request, pk):
    # Gets the records who have this ID
    accreditation_record = program_accreditation.objects.get(id=pk)

    #After getting that record, this code will delete it.
    accreditation_record.modified_by = request.user
    accreditation_record.deleted_at = timezone.now()
    accreditation_record.is_deleted=True
    accreditation_record.save()
    messages.success(request, f'The record is successfully archived!') 
    return redirect('accreditations:landing')


# --------------------------------- [ARCHIVE PAGE] --------------------------------- #

@login_required
@permission_required("Accreditation.delete_program_accreditation", raise_exception=True)
def archive_landing(request):
    #Getting the data from the API
    records = program_accreditation.objects.select_related('instrument_level', 'program').filter(is_deleted= True) #Getting all the data inside the Program table and storing it to the context variable

    # Initialize an empty list to store update forms for each record
    details = []

    # Iterate through each record and create an update form for it
    for record in records:
        update_form = ProgramAccreditation_UpdateForm(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form, created_by, modified_by))
        
    context = { 'records': records, 'details': details}  #Getting all the data inside the type table and storing it to the context variable

    return render(request, 'accreditation-page/program-accreditation/archive-page/landing-page.html', context)


@login_required
@permission_required("Accreditation.delete_program_accreditation", raise_exception=True)
def restore(request, pk):
    # Gets the records who have this ID
    accreditation_record = program_accreditation.objects.get(id=pk)

    #After getting that record, this code will delete it.
    accreditation_record.modified_by = request.user
    accreditation_record.deleted_at = None
    accreditation_record.is_deleted= False
    accreditation_record.save()
    messages.success(request, f'The record is successfully restored!') 
    return redirect('accreditations:accreditation-archive-page')

@login_required
@permission_required("Accreditation.delete_program_accreditation", raise_exception=True)
def destroy(request, pk):
    if request.method == 'POST':

        data = QueryDict(request.body.decode('utf-8'))
        entered_password = data.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                accreditation_record = program_accreditation.objects.get(id=pk)

                #After getting that record, this code will delete it.
                accreditation_record.delete()
                messages.success(request, f'Program Accreditation Record is permanently deleted!') 
                url_landing = "/accreditation/bodies/archive_page/"
                return JsonResponse({'success': True, 'url_landing': url_landing}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


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

        if passed_result_form.is_valid():
            length = request.POST.get('length')
            length = int(length)
            if length != 0:
                                # Get the current datetime in UTC timezone
                entry_result_at = accreditation_record.entry_result_at
                current_datetime = timezone.now()
                passed_result_form.instance.is_done = True
                passed_result_form.instance.is_visited = True
                passed_result_form.instance.entry_result_at = current_datetime

                # Get the modified datetime from the record
  

                # Make entry_result_at timezone-aware if it's not already
                # if entry_result_at.tzinfo is None:
                #     entry_result_at = entry_result_at.replace(tzinfo=timezone.utc)

                # Calculate the time difference
                time_difference = current_datetime - entry_result_at

                # Check if the time difference is less than or equal to 24 hours and if the date today is less than the revisit date
                if time_difference <= timedelta(hours=24) and current_datetime < accreditation_record.revisit_date:
                    passed_result_form.instance.revisit_date = None
                    print(timedelta(hours=23))
                    print(time_difference)
                    print (current_datetime)
                    print (entry_result_at)


                passed_result_form.save()

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
                return JsonResponse({'error': 'Please attach a file before submitting the form.'}, status=400)
            


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

        if revisit_result_form.is_valid():
            # Save the updated data to the database
            revisit_result_form.instance.modified_by = request.user
            revisit_result_form.instance.is_done = False
            revisit_result_form.instance.is_failed = False
            revisit_result_form.instance.is_visited = True
            revisit_result_form.instance.validity_date_from = None
            revisit_result_form.instance.validity_date_to = None
            current_datetime = timezone.now()
            revisit_result_form.instance.entry_result_at = current_datetime
            revisit_result_form.save()

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
        failed_result_form = FailedResult_Form(request.POST or None, instance=accreditation_record)

        if failed_result_form.is_valid():
            # Save the updated data to the database
            failed_result_form.instance.modified_by = request.user
            failed_result_form.instance.is_failed = True
            failed_result_form.instance.is_done = True
            current_datetime = timezone.now()
            failed_result_form.instance.entry_result_at = current_datetime
            failed_result_form.save()

            # Provide a success message as a JSON response
            messages.success(request, f'The Accreditation Result is successfully posted!') 
            return JsonResponse({"status": "success"}, status=200)

        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': failed_result_form.errors}, status=400)
        

@login_required
@permission_required("Accreditation.view_program_accreditation", raise_exception=True)
def result_page(request, pk):
    #Getting the data from the API
    passed_result_form = PassedResult_Form(request.POST or None)
    revisit_result_form = RevisitResult_Form(request.POST or None)
    failed_result_form = FailedResult_Form(request.POST or None)

    accreditation_record = program_accreditation.objects.get(id=pk)
    certificates_records = accreditation_certificates.objects.select_related('accredited_program').filter( accredited_program_id=pk, is_deleted= False) 
        
    context = { 
               'passed_result_form': passed_result_form,
               'failed_result_form': failed_result_form,
               'revisit_result_form': revisit_result_form,
               'records':  certificates_records,
               'accred_program': accreditation_record
               }  #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-page/accreditation-certificates/main-page/landing-page.html', context)