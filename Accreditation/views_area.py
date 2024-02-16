from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .models import area #Import the model for data retieving
from .forms import Create_Area_Form
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

class AreaList(PermissionRequiredMixin, View):

    permission_required = ["Accreditation.view_area", "Accreditation.add_area"]

    def get(self, request):
        #Getting the data from the API
        create_form = Create_Area_Form(request.POST or None)
        records = area.objects.filter(is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable

        # Initialize an empty list to store update forms for each record
        details = []

        # Iterate through each record and create an update form for it
        for record in records:
            update_form = Create_Area_Form(instance=record)
            created_by = record.created_by  # Get the user who created the record
            modified_by = record.modified_by  # Get the user who modified the record
            details.append((record, update_form, created_by, modified_by))
            
        context = { 'records': records, 'create_form': create_form, 'details': details}  #Getting all the data inside the type table and storing it to the context variable

        return render(request, 'accreditation-areas/main-page/landing-page.html', context)

    
    def post(self, request):
        create_form = Create_Area_Form(request.POST or None)

        if create_form.is_valid():
            create_form.instance.created_by = request.user
            create_form.save()
            name = create_form.cleaned_data.get('area_number')
            messages.success(request, f'{name} area is successfully created!') 
            return JsonResponse({'status': 'success'}, status=200)
        else:
            # Return a validation error using a JSON response
            return JsonResponse({'errors': create_form.errors}, status=400)
        
   
@login_required
@permission_required("Accreditation.change_area", raise_exception=True)
def update(request, pk):
# Retrieve the type object with the given primary key (pk)
    try:
        area_record = area.objects.get(id=pk)
    except area.DoesNotExist:
        return JsonResponse({'errors': 'area not found'}, status=404)

    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = Create_Area_Form(request.POST or None, instance=area_record)
        if update_form.is_valid():
            # Save the updated data to the database
            update_form.instance.modified_by = request.user
            update_form.save()  
            name = update_form.cleaned_data.get('area_number')

            # Provide a success message as a JSON response
            messages.success(request, f'{name} is successfully updated!') 
            return JsonResponse({'status': 'success'}, status=200)


        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)
        
@login_required
@permission_required("Accreditation.delete_area", raise_exception=True)
def archive(request, pk):
    # Gets the records who have this ID
    area_record = area.objects.get(id=pk)

    #After getting that record, this code will delete it.
    area_record.modified_by = request.user
    area_record.is_deleted=True
    area_record.deleted_at = timezone.now()
    name = area_record.area_number
    area_record.save()
    messages.success(request, f'{name} area is successfully archived!') 
    return redirect('accreditations:area-landing')



#------------------------------------------------------------[ ARCHIVE PAGE CODES ]------------------------------------------------------------#
@login_required
@permission_required("Accreditation.delete_area", raise_exception=True)
def archive_landing(request):
    records = area.objects.filter(is_deleted= True) #Getting all th

    details = []
     # Iterate through each record and create an update form for it
    for record in records:
        update_form = Create_Area_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form,created_by, modified_by))

    context = { 'details': details }#Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-areas/archive-page/landing-page.html', context)


@login_required
@permission_required("Accreditation.delete_area", raise_exception=True)
def restore(request, pk):
    # Gets the records who have this ID
    area_record =  area.objects.get(id=pk)

    #After getting that record, this code will restore it.
    area_record.modified_by = request.user
    area_record.deleted_at = None
    area_record.is_deleted=False
    name = area_record.area_number
    area_record.save()
    messages.success(request, f'{name} area is successfully restored!') 
    return redirect('accreditations:area-archive-page')


@login_required
@permission_required("Accreditation.delete_area", raise_exception=True)
def destroy(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                area_record =  area.objects.get(id=pk)

                #After getting that record, this code will delete it.
                area_record.delete()
                messages.success(request, f'Area is permanently deleted!') 
                url_landing = "/accreditation/area/archive-page/"
                return JsonResponse({'success': True, 'url_landing': url_landing}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


