from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from Users.models import activity_log
from .models import accredlevel #Import the model for data retieving
from .forms import Create_Level_Form
from django.contrib import messages
from .models import accredlevel
from .serializers import  AccredTypeSerializer
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
 

# Create your views here.
@login_required
def landing_page(request):
    #Getting all the data inside the type table and storing it to the context variable
    create_form = Create_Level_Form(request.POST or None)
    records = accredlevel.objects.filter(is_deleted=False) #Getting all the data inside the Program table and storing it to the context variable
   
    # Initialize an empty list to store update forms for each record
    update_forms = []

    # Iterate through each record and create an update form for it
    for record in records:
        update_form = Create_Level_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        update_forms.append((record, update_form, created_by, modified_by))

    context = { 'records': records, 'create_form': create_form, 'update_forms': update_forms}
    return render(request, 'accreditation_levels/landing_page.html', context)

@login_required
def create_level(request):
    create_form = Create_Level_Form(request.POST or None)
    if create_form.is_valid():
        create_form.instance.created_by = request.user
        create_form.save()
        name = create_form.cleaned_data.get('name')

        # Create an instance of the ActivityLog model
        activity_log_entry = activity_log()

        # Set the attributes of the instance
        activity_log_entry.module = "ACCREDITATION LEVEL MODULE"
        activity_log_entry.action = "Created a record"
        activity_log_entry.type = "CREATE"
        activity_log_entry.datetime_acted =  timezone.now()
        activity_log_entry.acted_by = request.user
        # Set other attributes as needed

        # Save the instance to the database
        activity_log_entry.save()


        messages.success(request, f'{name} accreditation level is successfully created!') 
        # url_landing = "{% url 'accreditations:type' %}"
        url_landing = "/accreditation/level/"
        return JsonResponse({'url_landing': url_landing}, status=200)

    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': create_form.errors}, status=400)

@login_required
def update_level(request, pk):
    # Retrieve the type object with the given primary key (pk)
    try:
        accreditation_level = accredlevel.objects.get(id=pk)
    except type.DoesNotExist:
        return JsonResponse({'errors': 'level not found'}, status=404)

    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = Create_Level_Form(request.POST or None, instance=accreditation_level)
        if update_form.is_valid():
            # Save the updated data to the database
            update_form.instance.modified_by = request.user
            update_form.save()
            type_name = update_form.cleaned_data.get('name')

            # Create an instance of the ActivityLog model
            activity_log_entry = activity_log()

            # Set the attributes of the instance
            activity_log_entry.module = "ACCREDITATION LEVEL MODULE"
            activity_log_entry.action = "Modified a record"
            activity_log_entry.type = "UPDATE"
            activity_log_entry.datetime_acted =  timezone.now()
            activity_log_entry.acted_by = request.user
            # Set other attributes as needed

            # Save the instance to the database
            activity_log_entry.save()

            # Provide a success message as a JSON response
            messages.success(request, f'{type_name} is successfully updated!') 
            return JsonResponse({'status': 'success'}, status=200)


        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)

@login_required
def archive_level(request, pk):
    # Gets the records who have this ID
    accreditation_level = accredlevel.objects.get(id=pk)

    #After getting that record, this code will delete it.
    accreditation_level.modified_by = request.user
    accreditation_level.is_deleted=True
    accreditation_level.deleted_at = timezone.now()
    name = accreditation_level.name
    accreditation_level.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "ACCREDITATION LEVEL MODULE"
    activity_log_entry.action = "Archived a record"
    activity_log_entry.type = "ARCHIVE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'{name} accreditation level is successfully archived!') 
    return redirect('accreditations:level-landing')


# --------------------------------- [ARCHIVE PAGE] --------------------------------- #
@login_required
def archive_level_page(request):
    records = accredlevel.objects.filter(is_deleted=True)

    details = []
     # Iterate through each record and create an update form for it
    for record in records:
        update_form = Create_Level_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form,created_by, modified_by))

    context = { 'details': details }#Getting all the data inside the type table and storing it to the context variable
    return render(request, 'level_archive_page/archive_landing.html', context)

@login_required
def restore_level(request, pk):
    # Gets the records who have this ID
    accreditation_level = accredlevel.objects.get(id=pk)

    #After getting that record, this code will restore it.
    accreditation_level.modified_by = request.user
    accreditation_level.deleted_at = None
    accreditation_level.is_deleted=False
    name = accreditation_level.name
    accreditation_level.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "ACCREDITATION LEVEL MODULE"
    activity_log_entry.action = "Restored a record"
    activity_log_entry.type = "RESTORE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()
    

    messages.success(request, f'{name} accreditation level is successfully restored!') 
    return redirect('accreditations:level-archive-page')

@login_required
def destroy_level(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                accreditation_level = accredlevel.objects.get(id=pk)

                #After getting that record, this code will delete it.
                accreditation_level.delete()

                # Create an instance of the ActivityLog model
                activity_log_entry = activity_log()

                # Set the attributes of the instance
                activity_log_entry.module = "ACCREDITATION LEVEL MODULE"
                activity_log_entry.action = "Permanently deleted a record"
                activity_log_entry.type = "DESTROY"
                activity_log_entry.datetime_acted =  timezone.now()
                activity_log_entry.acted_by = request.user
                # Set other attributes as needed

                # Save the instance to the database
                activity_log_entry.save()

                messages.success(request, f'Accreditation Level is permanently deleted!') 
                url_landing = "/accreditation/level/archive_page/"
                return JsonResponse({'success': True, 'url_landing': url_landing}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})