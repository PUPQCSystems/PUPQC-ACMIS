from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import accredtype #Import the model for data retieving
from .forms import Create_Type_Form
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def landing_page(request):
    return render(request, 'accreditation-instrument/landing_page.html')


@login_required
def update_page(request):
    return render(request, 'accreditation-instrument/landing_page.html')


