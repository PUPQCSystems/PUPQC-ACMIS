from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import accredtype #Import the model for data retieving
from .forms import Create_Type_Form
from django.contrib import messages
from .models import accredtype



# Create your views here.
        


def landing_page(request):
    #Getting all the data inside the type table and storing it to the context variable
    create_form = Create_Type_Form(request.POST or None)
    update_form = Create_Type_Form(request.POST or None)
    context = { 'records': accredtype.objects.filter(is_deleted=False), 'create_form': create_form, 'update_form': update_form}  #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation_type/type_landing.html', context)
    
def create_type(request):
    create_form = Create_Type_Form(request.POST or None)
    if create_form.is_valid():
        create_form.save()
        name = create_form.cleaned_data.get('name')
        messages.success(request, f'{name} accreditation type is successfully created!') 
        # url_landing = "{% url 'accreditation-type' %}"
        url_landing = "/accreditation/accreditation_type/"
        return JsonResponse({'url_landing': url_landing}, status=200)

    else:
        # Return a validation error using a JSON response
        return JsonResponse({'errors': create_form.errors}, status=400)


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
            update_form.save()
            type_name = update_form.cleaned_data.get('name')

            # Provide a success message as a JSON response
            messages.success(request, f'{type_name} is successfully updated!') 
            url_landing = "/accreditation/accreditation_type/"
            return JsonResponse({'url_landing': url_landing}, status=200)


        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)


def archive_type(request, pk):
    # Gets the records who have this ID
    accreditation_type = accredtype.objects.get(id=pk)

    #After getting that record, this code will delete it.
    accreditation_type.is_deleted=True
    name = accreditation_type.name
    accreditation_type.save()
    messages.success(request, f'{name} Accreditation Type is successfully archived!') 
    return redirect('accreditation-type-landing')


# --------------------------------- [ARCHIVE PAGE] --------------------------------- #

def archive_type_page(request):
    context = { 'records': accredtype.objects.filter(is_deleted=True)}  #Getting all the data inside the type table and storing it to the context variable
    return render(request, 'type_archive_page/archive_landing.html', context)


def restore_type(request, pk):
    # Gets the records who have this ID
    accreditation_type = accredtype.objects.get(id=pk)

    #After getting that record, this code will restore it.
    accreditation_type.is_deleted=False
    name = accreditation_type.name
    accreditation_type.save()
    messages.success(request, f'{name} Accreditation Type is successfully restored!') 
    return redirect('accreditation-type-archive-page')


def destroy_type(request, pk):
    # Gets the records who have this ID
    accreditation_type = accredtype.objects.get(id=pk)
    name = accreditation_type.name

    #After getting that record, this code will delete it.
    accreditation_type.delete()
    messages.success(request, f'{name} Accreditation Type is permanently deleted!') 
    return redirect('accreditation-type-archive-page')
