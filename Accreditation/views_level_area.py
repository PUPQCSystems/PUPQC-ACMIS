from django.utils import timezone
from django.views import View
from rest_framework import generics, viewsets, status
from django.shortcuts import render, redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import instrument, instrument_level, instrument_level_area #Import the model for data retieving
from Accreditation.serializers import InstrumentSerializer
from .forms import Create_Instrument_Form, Create_InstrumentLevel_Form, Create_LevelArea_Form, LevelAreaFormSet
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

class LevelAreaList(View):
    def get(self, request, pk):
        #Getting the data from the API
        formset  = LevelAreaFormSet(queryset=instrument_level_area.objects.none())
        records = instrument_level_area.objects.select_related('instrument_level').select_related('area').filter(instrument_level=pk, is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable

        # Initialize an empty list to store update forms for each record
        details = []

        # Iterate through each record and create an update form for it
        for record in records:
            update_form = Create_LevelArea_Form(instance=record)
            created_by = record.created_by  # Get the user who created the record
            modified_by = record.modified_by  # Get the user who modified the record
            details.append((record, update_form, created_by, modified_by))

        context = { 'records': records,'details': details, 'pk': pk, 'area_formset': formset}  #Getting all the data inside the type table and storing it to the context variable

        return render(request, 'accreditation-level-area/main-page/landing-page.html', context)
    
    def post(self, request, pk):

        formset = LevelAreaFormSet(data=self.request.POST)
        instrument_level_id = pk  # assign  the instrument_level ID
        for form in formset:
            form.instance.instrument_level_id = instrument_level_id
            form.instance.created_by = request.user

        if formset.is_valid():
            formset.save()  # Save the formset with the assigned foreign keys

            messages.success(request, f"Instrument's level areas is successfully created!")
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'formset_errors': formset.errors}, status=400)

@login_required
def update(request, pk):
# Retrieve the type object with the given primary key (pk)
    try:
        level_area = instrument_level_area.objects.get(id=pk)
    except instrument.DoesNotExist:
        return JsonResponse({'errors': 'instrument level not found'}, status=404)

    if request.method == 'POST':
        # Process the form submission with updated data
        update_form =  Create_LevelArea_Form(request.POST or None, instance = level_area)
        if update_form.is_valid():
            # Save the updated data to the database
            update_form.instance.modified_by = request.user
            name = level_area.area
            update_form.save()  

            # Provide a success message as a JSON response
            messages.success(request, f'{name} is successfully updated!') 
            return JsonResponse({'status': 'success'}, status=200)


        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)
        
@login_required
def archive(request, ins_pk, pk):
    # Gets the records who have this ID
    level_area = instrument_level_area.objects.get(id=pk)

    #After getting that record, this code will delete it.
    level_area.modified_by = request.user
    level_area.is_deleted=True
    level_area.deleted_at = timezone.now()
    name = level_area.area
    level_area.save()
    messages.success(request, f'{name} is successfully archived!') 
    return redirect('accreditations:instrument-level-area', pk=ins_pk)

#------------------------------------------------------------[ ARCHIVE PAGE CODES ]------------------------------------------------------------#
@login_required
def archive_landing(request, pk):
    records = instrument_level_area.objects.select_related('instrument_level').select_related('area').filter(instrument_level=pk, is_deleted= True) #Getting all the data inside the Program table and storing it to the context variable

    details = []
     # Iterate through each record and create an update form for it
    for record in records:
        update_form =  Create_LevelArea_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form,created_by, modified_by))

    context = { 'details': details, 'pk': pk , 'records': records}#Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-level-area/archive-page/landing-page.html', context)

@login_required
def restore(request, ins_pk, pk):
    # Gets the records who have this ID
    level_area = instrument_level_area.objects.get(id=pk)

    #After getting that record, this code will restore it.
    level_area.modified_by = request.user
    level_area.deleted_at = None
    level_area.is_deleted=False
    name = level_area.area
    level_area.save()
    messages.success(request, f'{name} is successfully restored!') 
    return redirect('accreditations:instrument-level-area-archive-page', pk=ins_pk)

@login_required
def destroy(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                level_area = instrument_level_area.objects.get(id=pk)
                name = level_area.area  #Get the name of the record

                #After getting that record, this code will delete it.
                level_area.delete()
                messages.success(request, f'{name} is permanently deleted!') 
                return JsonResponse({'success': True}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})