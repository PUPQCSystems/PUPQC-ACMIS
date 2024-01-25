from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from Accreditation.forms import ProgramAccreditation_Form, ProgramAccreditation_UpdateForm
from Accreditation.models import instrument, instrument_level, program_accreditation
from django.core.serializers import serialize
from django.contrib.auth import authenticate

# Create your views here.

@login_required
@permission_required("Accreditation.view_program_accreditation", raise_exception=True)
def landing_page(request):
    #Getting the data from the API
    create_form = ProgramAccreditation_Form(request.POST or None)
    records = program_accreditation.objects.select_related('instrument_level', 'program').filter(is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable

    # Initialize an empty list to store update forms for each record
    details = []

    # Iterate through each record and create an update form for it
    for record in records:
        update_form = ProgramAccreditation_UpdateForm(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form, created_by, modified_by))
        
    context = { 'records': records, 'create_form': create_form, 'details': details}  #Getting all the data inside the type table and storing it to the context variable

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
        instrument_records =  instrument.objects.filter(program=program_id, is_deleted=False)

    
        for instrument_record in instrument_records:
            instrument_id = instrument_record.id       
        instrument_levels = instrument_level.objects.filter(instrument_id =instrument_id, is_deleted=False)

        options = {}
        for choices_level in instrument_levels:
             option = choices_level.level.name +' - '+choices_level.instrument.name
             options[choices_level.id] = option

        print(options)


         #    Serialize the queryset to JSON

        # for instrument_record in instrument_records:
        #     instrument_id = instrument_record.id       
        # instrument_levels = list(instrument_level.objects.filter(instrument_id =instrument_id, is_deleted=False).values())

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
    if request.method == 'DELETE':

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





