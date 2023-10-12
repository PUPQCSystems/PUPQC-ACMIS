from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import accredlevel #Import the model for data retieving
from .forms import Create_Level_Form
from django.contrib import messages
from .models import accredlevel
from .serializers import  AccredTypeSerializer

# Create your views here.

def landing_page(request):
    #Getting all the data inside the type table and storing it to the context variable
    create_form = Create_Level_Form(request.POST or None)
    update_form = Create_Level_Form(request.POST or None)
    context = { 'records': accredlevel.objects.filter(is_deleted=False), 'create_form': create_form, 'update_form': update_form}  #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation_levels/landing_page.html', context)
    
def create_level(request):
    create_form = Create_Level_Form(request.POST or None)
    if create_form.is_valid():
        create_form.save()
        name = create_form.cleaned_data.get('name')
        messages.success(request, f'{name} accreditation level is successfully created!') 
        # url_landing = "{% url 'accreditation-type' %}"
        url_landing = "/accreditation/accreditation_level/"
        return JsonResponse({'url_landing': url_landing}, status=200)

    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': create_form.errors}, status=400)


def update_level(request, pk):
    # Retrieve the type object with the given primary key (pk)
    try:
        accreditation_level = accredlevel.objects.get(id=pk)
    except type.DoesNotExist:
        return JsonResponse({'errors': 'level not found'}, status=404)

    # Create an instance of the form with the type data
    # update_form = Create_Level_Form(instance=type)
    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = Create_Level_Form(request.POST or None, instance=accreditation_level)
        if update_form.is_valid():
            # Save the updated data to the database
            update_form.save()
            type_name = update_form.cleaned_data.get('name')

            # Provide a success message as a JSON response
            messages.success(request, f'{type_name} is successfully updated!') 
            url_landing = "/accreditation/accreditation_level/"
            return JsonResponse({'url_landing': url_landing}, status=200)


        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)


def archive_level(request, pk):
    # Gets the records who have this ID
    accreditation_level = accredlevel.objects.get(id=pk)

    #After getting that record, this code will delete it.
    accreditation_level.is_deleted=True
    name = accreditation_level.name
    accreditation_level.save()
    messages.success(request, f'{name} accreditation level is successfully archived!') 
    return redirect('accreditation-level-landing')


# --------------------------------- [ARCHIVE PAGE] --------------------------------- #

def archive_level_page(request):
    context = { 'records': accredlevel.objects.filter(is_deleted=True)}  #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'level_archive_page/archive_landing.html', context)


def restore_level(request, pk):
    # Gets the records who have this ID
    accreditation_level = accredlevel.objects.get(id=pk)

    #After getting that record, this code will restore it.
    accreditation_level.is_deleted=False
    name = accreditation_level.name
    accreditation_level.save()
    messages.success(request, f'{name} accreditation level is successfully restored!') 
    return redirect('accreditation-level-archive-page')


def destroy_level(request, pk):
    # Gets the records who have this ID
    accreditation_level = accredlevel.objects.get(id=pk)
    name = accreditation_level.name

    #After getting that record, this code will delete it.
    accreditation_level.delete()
    messages.success(request, f'{name} accreditation level is permanently deleted!') 
    return redirect('accreditation-level-archive-page')
