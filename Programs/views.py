from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Program #Import the model for data retieving
from .forms import CreateForm
from django.contrib import messages

# Create your views here.

def landing_page(request):
  #Getting all the data inside the Program table and storing it to the context variable
    create_form = CreateForm(request.POST or None)
    update_form = CreateForm(request.POST or None)
    context = { 'records': Program.objects.all(), 'create_form': create_form, 'update_form': update_form}  #Getting all the data inside the Program table and storing it to the context variable
    return render(request, 'landing_page/landing_page.html', context)

def create_program(request):
    create_form = CreateForm(request.POST or None)
    if create_form.is_valid():
        create_form.save()
        program_name = create_form.cleaned_data.get('abbreviation')
        # messages.success(request, f'{program_name} is successfully created!') 
        # return HttpResponseRedirect('/Programs/landing_page/')
        return JsonResponse({'toastr_message': 'Program created successfully!'})
    
    else:
        # Return a validation error using a JSON response

        return JsonResponse({'errors': create_form.errors}, status=400)
    

    # context = { 'records': Program.objects.all(), 'create_form': create_form}  #Getting all the data inside the Program table and storing it to the context variable
    # return render(request, 'landing_page/landing_page.html', context)


def update_program(request, pk):  
    create_form = CreateForm(request.POST or None)

    program = Program.objects.all()
    update_form = CreateForm(instance=program)

    if request.method == 'POST':
      update_form = CreateForm(request.POST, instance=program)
      if update_form.is_valid():
          update_form.save()
          program_name = update_form.cleaned_data.get('abbreviation')
          messages.success(request, f'{program_name} is successfully updated!') 
          return HttpResponseRedirect('/Programs/landing_page/')

    context = { 'records': Program.objects.all(), 'create_form': create_form, 'update_form': update_form}  #Getting all the data inside the Program table and storing it to the context variable
    return render(request, 'landing_page/landing_page.html', context)

