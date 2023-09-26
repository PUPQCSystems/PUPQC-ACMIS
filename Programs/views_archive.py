from django.shortcuts import render, redirect
# from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Programs #Import the model for data retieving
# from .forms import CreateForm
from django.contrib import messages

# Create your views here.

#-----------------------------[Archive Page Functions]----------------------------#
def landing_page(request):
    context = { 'records': Programs.objects.filter(is_deleted=True)}  #Getting all the data inside the Program table and storing it to the context variable
    return render(request, 'archive_page/archive_landing.html', context)


def restore_program(request, pk):
    # Gets the records who have this ID
    program = Programs.objects.get(id=pk)

    #After getting that record, this code will restore it.
    program.is_deleted=False
    program.save()
    messages.success(request, f'Program is successfully restored!') 
    return redirect('archive-landing')


def destroy_program(request, pk):
    # Gets the records who have this ID
    program = Programs.objects.get(id=pk)

    #After getting that record, this code will delete it.
    program.delete()
    messages.success(request, f'Program is permanently deleted!') 
    return redirect('archive-landing')
