from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import accredbodies #Import the model for data retieving
from .forms import Create_Bodies_Form
from django.contrib import messages
from .serializers import  AccredTypeSerializer
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.http import QueryDict

# Create your views here.

@login_required
@permission_required("Accreditation.view_accredbodies", raise_exception=True)
def landing_page(request):
    #Getting all the data inside the type table and storing it to the context variable
    create_form = Create_Bodies_Form(request.POST or None)
    records = accredbodies.objects.filter(is_deleted=False) #Getting all the data inside the Program table and storing it to the context variable
   
    # Initialize an empty list to store update forms for each record
    update_forms = []

    # Iterate through each record and create an update form for it
    for record in records:
        update_form = Create_Bodies_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        update_forms.append((record, update_form, created_by, modified_by))
    
    context = { 'records': records, 'create_form': create_form, 'update_forms': update_forms}  #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation_bodies/landing_page.html', context)
    
@login_required
@permission_required("Accreditation.add_accredbodies", raise_exception=True)
def create_bodies(request):
    create_form = Create_Bodies_Form(request.POST or None)
    if create_form.is_valid():
        create_form.instance.created_by = request.user
        create_form.save()
        abbreviation = create_form.cleaned_data.get('abbreviation')
        messages.success(request, f'{abbreviation} accreditation body is successfully created!') 
        # url_landing = "{% url 'accreditations:type' %}"
        url_landing = "/accreditation/bodies/"
        return JsonResponse({'url_landing': url_landing}, status=200)

    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': create_form.errors}, status=400)

@login_required
@permission_required("Accreditation.change_accredbodies", raise_exception=True)
def update_bodies(request, pk):
    # Retrieve the type object with the given primary key (pk)
    try:
        accreditation_body = accredbodies.objects.get(id=pk)
    except type.DoesNotExist:
        return JsonResponse({'errors': 'Acrreditation body not found'}, status=404)

    # Create an instance of the form with the type data
    # update_form = Create_Bodies_Form(instance=type)
    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = Create_Bodies_Form(request.POST or None, instance=accreditation_body)
        if update_form.is_valid():
            # Save the updated data to the database
            update_form.instance.modified_by = request.user
            update_form.save()
            abbreviation = update_form.cleaned_data.get('abbreviation')

            # Provide a success message as a JSON response
            messages.success(request, f'{abbreviation} is successfully updated!') 

            return JsonResponse({"status": "success"}, status=200)

        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)
        

@login_required
@permission_required("Accreditation.delete_accredbodies", raise_exception=True)
def archive_bodies(request, pk):
    # Gets the records who have this ID
    accreditation_body = accredbodies.objects.get(id=pk)

    #After getting that record, this code will delete it.
    accreditation_body.modified_by = request.user
    accreditation_body.deleted_at = timezone.now()
    accreditation_body.is_deleted=True
    abbreviation = accreditation_body.abbreviation
    accreditation_body.save()
    messages.success(request, f'{abbreviation} accreditation bodies is successfully archived!') 
    return redirect('accreditations:bodies-landing')


# --------------------------------- [ARCHIVE PAGE] --------------------------------- #

@login_required
@permission_required("Accreditation.delete_accredbodies", raise_exception=True)
def archive_landing(request):
    records = accredbodies.objects.filter(is_deleted=True)

    details = []
     # Iterate through each record and create an update form for it
    for record in records:
        update_form = Create_Bodies_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form, created_by, modified_by))

    context = { 'details': details }#Getting all the data inside the type table and storing it to the context variable
    return render(request, 'bodies_archive_page/archive_landing.html', context)

@login_required
@permission_required("Accreditation.delete_accredbodies", raise_exception=True)
def restore_bodies(request, pk):
    # Gets the records who have this ID
    accreditation_body = accredbodies.objects.get(id=pk)

    #After getting that record, this code will restore it.
    accreditation_body.modified_by = request.user
    accreditation_body.deleted_at = None
    accreditation_body.is_deleted=False
    abbreviation = accreditation_body.abbreviation
    accreditation_body.save()
    messages.success(request, f'{abbreviation} accreditation bodies is successfully restored!') 
    return redirect('accreditations:bodies-archive-page')

@login_required
@permission_required("Accreditation.delete_accredbodies", raise_exception=True)
def destroy_bodies(request, pk):
    if request.method == 'DELETE':

        data = QueryDict(request.body.decode('utf-8'))
        entered_password = data.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                accreditation_bodies = accredbodies.objects.get(id=pk)

                #After getting that record, this code will delete it.
                accreditation_bodies.delete()
                messages.success(request, f'Accreditation Body is permanently deleted!') 
                url_landing = "/accreditation/bodies/archive_page/"
                return JsonResponse({'success': True, 'url_landing': url_landing}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})