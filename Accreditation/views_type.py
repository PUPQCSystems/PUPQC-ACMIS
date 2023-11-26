from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import accredtype #Import the model for data retieving
from .forms import Create_Type_Form
from django.contrib import messages
from .models import accredtype
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
 

# Create your views here.
        

@login_required
def landing_page(request):
    #Getting all the data inside the type table and storing it to the context variable
    create_form = Create_Type_Form(request.POST or None)
    records = accredtype.objects.filter(is_deleted=False) #Getting all the data inside the Program table and storing it to the context variable
   
    # Initialize an empty list to store update forms for each record
    update_forms = []

    # Iterate through each record and create an update form for it
    for record in records:
        update_form = Create_Type_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        update_forms.append((record, update_form, created_by, modified_by))
        
    context = { 'records': records, 'create_form': create_form, 'update_forms': update_forms}  #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation_type/type_landing.html', context)
    
@login_required
def create_type(request):
    create_form = Create_Type_Form(request.POST or None)
    if create_form.is_valid():
        create_form.instance.created_by = request.user
        create_form.save()
        name = create_form.cleaned_data.get('name')
        messages.success(request, f'{name} accreditation type is successfully created!') 
        # url_landing = "{% url 'accreditations:type' %}"
        url_landing = "/accreditation/type/"
        return JsonResponse({'url_landing': url_landing}, status=200)

    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': create_form.errors}, status=400)

@login_required
def update_type(request, pk):
    # Retrieve the type object with the given primary key (pk)
    try:
        accreditation_type = accredtype.objects.get(id=pk)
    except type.DoesNotExist:
        return JsonResponse({'errors': 'type not found'}, status=404)

    # Create an instance of the form with the type data
    # update_form = Create_Type_Form(instance=type)
    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = Create_Type_Form(request.POST or None, instance=accreditation_type)
        if update_form.is_valid():
            # Save the updated data to the database
            update_form.instance.modified_by = request.user
            update_form.save()
            type_name = update_form.cleaned_data.get('name')

            # Provide a success message as a JSON response
            messages.success(request, f'{type_name} is successfully updated!') 
            url_landing = "/accreditation/type/"
            return JsonResponse({'url_landing': url_landing}, status=200)


        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)

@login_required
def archive_type(request, pk):
    # Gets the records who have this ID
    accreditation_type = accredtype.objects.get(id=pk)

    #After getting that record, this code will delete it.
    accreditation_type.modified_by = request.user
    accreditation_type.deleted_at = timezone.now()
    accreditation_type.is_deleted=True
    name = accreditation_type.name
    accreditation_type.save()
    messages.success(request, f'{name} Accreditation Type is successfully archived!') 
    return redirect('accreditations:type-landing')


# --------------------------------- [ARCHIVE PAGE] --------------------------------- #
@login_required
def archive_type_page(request):
    records =  accredtype.objects.filter(is_deleted=True)

    details = []
     # Iterate through each record and create an update form for it
    for record in records:
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, created_by, modified_by))

    context = { 'details': details }#Getting all the data inside the type table and storing it to the context variable
    return render(request, 'type_archive_page/archive_landing.html', context)

@login_required
def restore_type(request, pk):
    # Gets the records who have this ID
    accreditation_type = accredtype.objects.get(id=pk)

    #After getting that record, this code will restore it.
    accreditation_type.modified_by = request.user
    accreditation_type.is_deleted=False
    accreditation_type.deleted_at = None
    name = accreditation_type.name
    accreditation_type.save()
    messages.success(request, f'{name} Accreditation Type is successfully restored!') 
    return redirect('accreditations:type-archive-page')

@login_required
def destroy_type(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                accreditation_type = accredtype.objects.get(id=pk)

                #After getting that record, this code will delete it.
                accreditation_type.delete()
                messages.success(request, f'Accreditation Type is permanently deleted!') 
                url_landing = "/accreditation/type/archive_page/"
                return JsonResponse({'success': True, 'url_landing': url_landing}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})