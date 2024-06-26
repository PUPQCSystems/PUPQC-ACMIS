from django.utils import timezone
from django.views import View
from django.shortcuts import render, redirect, render, get_object_or_404
from django.http import JsonResponse
from .models import instrument, instrument_level, instrument_level_area #Import the model for data retieving
from .forms import Create_InstrumentLevel_Form, Create_LevelArea_Form, LevelAreaFormSet
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

class InstrumentLevelList(View):
    

    def get(self, request, pk):
        #Getting the data from the API
        instrumentlevel_form = Create_InstrumentLevel_Form(request.POST or None)
        levelarea_form = Create_LevelArea_Form(request.POST or None)
        formset  = LevelAreaFormSet(queryset=instrument_level_area.objects.none())
        records = instrument_level.objects.select_related('instrument').filter(instrument=pk,is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable

        # Initialize an empty list to store update forms for each record
        details = []

        # Iterate through each record and create an update form for it
        for record in records:
            update_form = Create_InstrumentLevel_Form(instance=record)
            created_by = record.created_by  # Get the user who created the record
            modified_by = record.modified_by  # Get the user who modified the record
            details.append((record, update_form, created_by, modified_by))

        context = { 'records': records, 'instrumentlevel_form': instrumentlevel_form, 'levelarea_form': levelarea_form , 'details': details, 'pk': pk, 'area_formset': formset}  #Getting all the data inside the type table and storing it to the context variable

        return render(request, 'accreditation-instrument-level/main-page/landing-page.html', context)
    
    def post(self, request, pk):
        instrumentlevel_form = Create_InstrumentLevel_Form(request.POST or None)
        formset = LevelAreaFormSet(data=self.request.POST)

        if instrumentlevel_form.is_valid() and formset.is_valid():
            instrumentlevel_form.instance.created_by = request.user
            instrumentlevel_form.instance.instrument_id = pk
            instrumentlevel = instrumentlevel_form.save()  # Save and capture the instance

            instrument_level_id = instrumentlevel.id  # Get the ID 

            for form in formset:
                form.instance.instrument_level_id = instrument_level_id
                form.instance.created_by = request.user

            formset.save()  # Save the formset with the assigned foreign keys

            messages.success(request, f"Accreditation instrument's level is successfully created!")
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'instrumentlevel_errors': instrumentlevel_form.errors, 'formset_errors': formset.errors}, status=400)

@login_required
# @permission_required("Accreditation.change_instrument_level", raise_exception=True)
def update(request, pk):
# Retrieve the type object with the given primary key (pk)
    try:
        accreditation_instrumentlevel = instrument_level.objects.get(id=pk)
    except instrument.DoesNotExist:
        return JsonResponse({'errors': 'instrument level not found'}, status=404)

    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = Create_InstrumentLevel_Form(request.POST or None, instance=accreditation_instrumentlevel)
        if update_form.is_valid():
            # Save the updated data to the database
            update_form.instance.modified_by = request.user
            update_form.save()  
            name = update_form.cleaned_data.get('level')

            # Provide a success message as a JSON response
            messages.success(request, f'{name} is successfully updated!') 
            return JsonResponse({'status': 'success'}, status=200)


        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)
        
@login_required
# @permission_required("Accreditation.delete_instrument_level", raise_exception=True)
def archive(request, ins_pk, pk):
    # Gets the records who have this ID
    accreditation_instrument = instrument_level.objects.get(id=pk)

    #After getting that record, this code will delete it.
    accreditation_instrument.modified_by = request.user
    accreditation_instrument.is_deleted=True
    accreditation_instrument.deleted_at = timezone.now()
    name = accreditation_instrument.level
    accreditation_instrument.save()
    messages.success(request, f'{name} accreditation instrument level is successfully archived!') 
    return redirect('accreditations:instrument-level', pk=ins_pk)

#------------------------------------------------------------[ ARCHIVE PAGE CODES ]------------------------------------------------------------#
@login_required
# @permission_required("Accreditation.delete_instrument_level", raise_exception=True)
def archive_landing(request, pk):
    records = instrument_level.objects.select_related('instrument').filter(instrument=pk, is_deleted= True)

    details = []
     # Iterate through each record and create an update form for it
    for record in records:
        update_form = Create_InstrumentLevel_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form,created_by, modified_by))

    context = { 'details': details, 'pk': pk , 'records': records}#Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-instrument-level/archive-page/landing-page.html', context)

@login_required
# @permission_required("Accreditation.delete_instrument_level", raise_exception=True)
def restore(request, ins_pk, pk):
    # Gets the records who have this ID
    accreditation_instrumentlevel = instrument_level.objects.get(id=pk)

    #After getting that record, this code will restore it.
    accreditation_instrumentlevel.modified_by = request.user
    accreditation_instrumentlevel.deleted_at = None
    accreditation_instrumentlevel.is_deleted=False
    name = accreditation_instrumentlevel.level
    accreditation_instrumentlevel.save()
    messages.success(request, f'{name} accreditation level is successfully restored!') 
    return redirect('accreditations:instrument-level-archive-page', pk=ins_pk)

@login_required
# @permission_required("Accreditation.delete_instrument_level", raise_exception=True)
def destroy(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                accreditation_instrumentlevel = instrument_level.objects.get(id=pk)

                #After getting that record, this code will delete it.
                accreditation_instrumentlevel.delete()
                messages.success(request, f'Instrument Level is permanently deleted!') 
                return JsonResponse({'success': True}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})