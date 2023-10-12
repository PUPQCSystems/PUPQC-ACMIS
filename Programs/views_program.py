from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Programs #Import the model for data retieving
from .forms import CreateForm
from django.contrib import messages
from .models import Programs
from .serializers import ProgramSerializer

# Create your views here.

def landing_page(request):
  #Getting all the data inside the Program table and storing it to the context variable
    create_form = CreateForm(request.POST or None)
    update_form = CreateForm(request.POST or None)
    context = { 'records': Programs.objects.filter(is_deleted=False), 'create_form': create_form, 'update_form': update_form}  #Getting all the data inside the Program table and storing it to the context variable
    return render(request, 'program_page/program_landing.html', context)

def create_program(request):
    create_form = CreateForm(request.POST or None)
    if create_form.is_valid():
        create_form.save()
        program_name = create_form.cleaned_data.get('abbreviation')

        # return redirect('/Programs/landing_page/')
        # return JsonResponse({'toastr_message': program_name + ' Program created successfully!'}, status=200)
        messages.success(request, f'{program_name} is successfully created!') 
        url_landing = "/programs/program_page/"
        return JsonResponse({'url_landing': url_landing}, status=200)

    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': create_form.errors}, status=400)


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
            update_form.save()
            program_name = update_form.cleaned_data.get('abbreviation')

            # Provide a success message as a JSON response
            messages.success(request, f'{program_name} is successfully updated!') 
            url_landing = "/programs/program_page/"
            return JsonResponse({'url_landing': url_landing}, status=200)


        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)


def archive_program(request, pk):
    # Gets the records who have this ID
    program = Programs.objects.get(id=pk)

    #After getting that record, this code will delete it.
    program.is_deleted=True
    program.save()
    messages.success(request, f'Program is successfully archived!') 
    return redirect('program-landing')


#-----------------------------[Archive Page Functions]----------------------------#
def archive_page(request):
    context = { 'records': Programs.objects.filter(is_deleted=True)}  #Getting all the data inside the Program table and storing it to the context variable
    return render(request, 'archive_page/archive_landing.html', context)


def restore_program(request, pk):
    # Gets the records who have this ID
    program = Programs.objects.get(id=pk)

    #After getting that record, this code will restore it.
    program.is_deleted=False
    program.save()
    messages.success(request, f'Program is successfully restored!') 
    return redirect('archive-page')


def destroy_program(request, pk):
    # Gets the records who have this ID
    program = Programs.objects.get(id=pk)

    #After getting that record, this code will delete it.
    program.delete()
    messages.success(request, f'Program is permanently deleted!') 
    return redirect('archive-page')
