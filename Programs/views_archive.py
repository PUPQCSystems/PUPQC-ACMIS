from django.shortcuts import render, redirect
# from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Programs #Import the model for data retieving
from .forms import CreateForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

#-----------------------------[Archive Page Functions]----------------------------#
@login_required
@permission_required("Programs.change_programs | Programs.delete_programs", raise_exception=True)
def landing_page(request):
    records = Programs.objects.filter(is_deleted=True)

    details = []
     # Iterate through each record and create an update form for it
    for record in records:
        update_form = CreateForm(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form, created_by, modified_by))

    context = { 'details': details }#Getting all the data inside the type table and storing it to the context variable
    return render(request, 'archive_page/archive_landing.html', context)

@login_required
@permission_required("Programs.delete_programs", raise_exception=True)
def restore_program(request, pk):
    # Gets the records who have this ID
    program = Programs.objects.get(id=pk)

    #After getting that record, this code will restore it.
    program.modified_by = request.user
    program.is_deleted=False
    program.deleted_at = None
    program.save()
    messages.success(request, f'Program is successfully restored!') 
    return redirect('programs:archive-landing')

@login_required
@permission_required("Programs.delete_programs", raise_exception=True)
def destroy_program(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                program = Programs.objects.get(id=pk)

                #After getting that record, this code will delete it.
                program.delete()
                messages.success(request, f'Program is permanently deleted!') 
                url_landing = "/programs/archive_page/"
                return JsonResponse({'success': True, 'url_landing': url_landing}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})
