from django.utils import timezone
from django.views import View

from django.shortcuts import render, redirect, render, get_object_or_404
from django.http import  JsonResponse
from .models import instrument_level_area, level_area_parameter #Import the model for data retieving
from Accreditation.serializers import InstrumentSerializer
from .forms import AreaParameterFormSet, AreaParameter_Form
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


class AreaParameterList(View):
    def get(self, request, pk):
        #Getting the data from the API
        formset  = AreaParameterFormSet(queryset=level_area_parameter.objects.none())
        records = level_area_parameter.objects.select_related('instrument_level_area').select_related('parameter').filter(instrument_level_area=pk, is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable

        # Initialize an empty list to store update forms for each record
        details = []

        # Iterate through each record and create an update form for it
        for record in records:
            update_form = AreaParameter_Form(instance=record)
            created_by = record.created_by  # Get the user who created the record
            modified_by = record.modified_by  # Get the user who modified the record
            details.append((record, update_form, created_by, modified_by))

        context = { 'records': records,'details': details, 'pk': pk, 'formset': formset}  #Getting all the data inside the type table and storing it to the context variable

        return render(request, 'accreditation-level-area-parameter/main-page/landing-page.html', context)
    
    def post(self, request, pk):
        formset = AreaParameterFormSet(data=self.request.POST)
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
        

class AreaParameterList(View):
    def get(self, request, pk):
        #Getting the data from the API
        formset  = AreaParameterFormSet(queryset=level_area_parameter.objects.none())
        records = level_area_parameter.objects.select_related('instrument_level_area').select_related('parameter').filter(instrument_level_area=pk, is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable

        # Initialize an empty list to store update forms for each record
        details = []

        # Iterate through each record and create an update form for it
        for record in records:
            update_form = AreaParameter_Form(instance=record)
            created_by = record.created_by  # Get the user who created the record
            modified_by = record.modified_by  # Get the user who modified the record
            details.append((record, update_form, created_by, modified_by))

        context = { 'records': records,'details': details, 'pk': pk, 'formset': formset}  #Getting all the data inside the type table and storing it to the context variable

        return render(request, 'accreditation-level-area-parameter/main-page/landing-page.html', context)
    
    def post(self, request, pk):
        formset = AreaParameterFormSet(data=self.request.POST)
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
        area_parameter = level_area_parameter.objects.get(id=pk)
    except level_area_parameter.DoesNotExist:
        return JsonResponse({'errors': 'Parameter not found'}, status=404)

    if request.method == 'POST':
        # Process the form submission with updated data
        update_form =  AreaParameter_Form(request.POST or None, instance = area_parameter)
        if update_form.is_valid():
            # Save the updated data to the database
            update_form.instance.modified_by = request.user
            name = area_parameter.parameter
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
    area_parameter = instrument_level_area.objects.get(id=pk)

    #After getting that record, this code will delete it.
    area_parameter.modified_by = request.user
    area_parameter.is_deleted=True
    area_parameter.deleted_at = timezone.now()
    name = area_parameter.area
    area_parameter.save()
    messages.success(request, f'{name} is successfully archived!') 
    return redirect('accreditations:instrument-level-area-parameter', pk=ins_pk)

#------------------------------------------------------------[ ARCHIVE PAGE CODES ]------------------------------------------------------------#
@login_required
def archive_landing(request, pk):
    records = instrument_level_area.objects.select_related('instrument_level').select_related('area').filter(instrument_level=pk, is_deleted= True) #Getting all the data inside the Program table and storing it to the context variable

    details = []
     # Iterate through each record and create an update form for it
    for record in records:
        update_form =  AreaParameter_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form,created_by, modified_by))

    context = { 'details': details, 'pk': pk , 'records': records}#Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-level-area-parameter/archive-page/landing-page.html', context)

@login_required
def restore(request, ins_pk, pk):
    # Gets the records who have this ID
    area_parameter = instrument_level_area.objects.get(id=pk)

    #After getting that record, this code will restore it.
    area_parameter.modified_by = request.user
    area_parameter.deleted_at = None
    area_parameter.is_deleted=False
    name = area_parameter.area
    area_parameter.save()
    messages.success(request, f'{name} is successfully restored!') 
    return redirect('accreditations:instrument-level-area-parameter-archive-page', pk=ins_pk)

@login_required
def destroy(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                area_parameter = instrument_level_area.objects.get(id=pk)
                name = area_parameter.area  #Get the name of the record

                #After getting that record, this code will delete it.
                area_parameter.delete()
                messages.success(request, f'{name} is permanently deleted!') 
                return JsonResponse({'success': True}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})