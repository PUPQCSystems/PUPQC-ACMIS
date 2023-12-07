from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Programs #Import the model for data retieving
from .forms import CreateForm
from django.contrib import messages
from .models import Programs
from django.utils import timezone
from .serializers import ProgramSerializer
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def landing_page(request):
  #Getting all the data inside the Program table and storing it to the context variable
    create_form = CreateForm(request.POST or None)
    records = Programs.objects.filter(is_deleted=False) #Getting all the data inside the Program table and storing it to the context variable
   
    # Initialize an empty list to store update forms for each record
    update_forms = []

    # Iterate through each record and create an update form for it
    for record in records:
        update_form = CreateForm(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        update_forms.append((record, update_form, created_by, modified_by))
  
    context = {'records': records, 'create_form': create_form, 'update_forms': update_forms}  
    return render(request, 'program_page/program_landing.html', context)


#This is the function for creating the record
@login_required
def create_program(request):
    create_form = CreateForm(request.POST or None)
    
    if create_form.is_valid():
        create_form.instance.created_by = request.user
        create_form.save()
        program_name = create_form.cleaned_data.get('abbreviation')

        # return redirect('/Programs/landing_page/')
        # return JsonResponse({'toastr_message': program_name + ' Program created successfully!'}, status=200)
        messages.success(request, f'{program_name} is successfully created!') 
        url_landing = "/programs/"
        return JsonResponse({'url_landing': url_landing}, status=200)

    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': create_form.errors}, status=400)

#This is the function for updating the record
@login_required
def update_program(request, pk):
    # Retrieve the program object with the given primary key (pk)
    try:
        program = Programs.objects.get(id=pk)
    except Programs.DoesNotExist:
        return JsonResponse({'errors': 'Program not found'}, status=404)

    # Create an instance of the form with the program data
    # update_form = CreateForm(instance=program)
    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = CreateForm(request.POST or None, instance=program)
        if update_form.is_valid():
            # Save the updated data to the database
            update_form.instance.modified_by = request.user
            update_form.save()
            program_name = update_form.cleaned_data.get('abbreviation')

            # Provide a success message as a JSON response
            messages.success(request, f'{program_name} is successfully updated!') 
            url_landing = "/programs/"
            return JsonResponse({'url_landing': url_landing}, status=200)


        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)

@login_required
def archive_program(request, pk):
    # Gets the records who have this ID
    program = Programs.objects.get(id=pk)

    #After getting that record, this code will delete it.
    program.modified_by = request.user
    program.deleted_at = timezone.now()
    program.is_deleted=True
    program.save()
    messages.success(request, f'Program is successfully archived!') 
    return redirect('programs:landing')
