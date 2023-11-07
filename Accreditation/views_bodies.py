from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import accredbodies #Import the model for data retieving
from .forms import Create_Bodies_Form
from django.contrib import messages
from .serializers import  AccredTypeSerializer

# Create your views here.

def landing_page(request):
    #Getting all the data inside the type table and storing it to the context variable
    create_form = Create_Bodies_Form(request.POST or None)
    update_form = Create_Bodies_Form(request.POST or None)
    context = { 'records': accredbodies.objects.filter(is_deleted=False), 'create_form': create_form, 'update_form': update_form}  #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation_bodies/landing_page.html', context)
    
def create_bodies(request):
    create_form = Create_Bodies_Form(request.POST or None)
    if create_form.is_valid():
        create_form.save()
        abbreviation = create_form.cleaned_data.get('abbreviation')
        messages.success(request, f'{abbreviation} accreditation body is successfully created!') 
        # url_landing = "{% url 'accreditation-type' %}"
        url_landing = "/accreditation/accreditation_bodies/"
        return JsonResponse({'url_landing': url_landing}, status=200)

    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': create_form.errors}, status=400)


def update_bodies(request, pk):
    # Retrieve the type object with the given primary key (pk)
    try:
        accreditation_body = accredbodies.objects.get(id=pk)
    except type.DoesNotExist:
        return JsonResponse({'errors': 'bodies not found'}, status=404)

    # Create an instance of the form with the type data
    # update_form = Create_Bodies_Form(instance=type)
    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = Create_Bodies_Form(request.POST or None, instance=accreditation_body)
        if update_form.is_valid():
            # Save the updated data to the database
            update_form.save()
            abbreviation = update_form.cleaned_data.get('abbreviation')

            # Provide a success message as a JSON response
            messages.success(request, f'{abbreviation} is successfully updated!') 
            url_landing = "/accreditation/accreditation_bodies/"
            return JsonResponse({'url_landing': url_landing}, status=200)

        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)
        


def archive_bodies(request, pk):
    # Gets the records who have this ID
    accreditation_body = accredbodies.objects.get(id=pk)

    #After getting that record, this code will delete it.
    accreditation_body.is_deleted=True
    abbreviation = accreditation_body.abbreviation
    accreditation_body.save()
    messages.success(request, f'{abbreviation} accreditation bodies is successfully archived!') 
    return redirect('accreditation-bodies-landing')


# --------------------------------- [ARCHIVE PAGE] --------------------------------- #

def archive_landing(request):
    context = { 'records': accredbodies.objects.filter(is_deleted=True)}  #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'bodies_archive_page/archive_landing.html', context)


def restore_bodies(request, pk):
    # Gets the records who have this ID
    accreditation_body = accredbodies.objects.get(id=pk)

    #After getting that record, this code will restore it.
    accreditation_body.is_deleted=False
    abbreviation = accreditation_body.abbreviation
    accreditation_body.save()
    messages.success(request, f'{abbreviation} accreditation bodies is successfully restored!') 
    return redirect('accreditation-bodies-archive-page')


def destroy_bodies(request, pk):
    # Gets the records who have this ID
    accreditation_bodies = accredbodies.objects.get(id=pk)
    abbreviation = accreditation_bodies.abbreviation

    #After getting that record, this code will delete it.
    accreditation_bodies.delete()
    messages.success(request, f'{abbreviation} accreditation body is permanently deleted!') 
    return redirect('accreditation-bodies-archive-page')
