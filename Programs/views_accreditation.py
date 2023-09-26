from django.shortcuts import render, redirect
# from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from .models import Programs #Import the model for data retieving
# from .forms import CreateForm
# from django.contrib import messages

# Create your views here.

def landing_page(request):
    return render(request, 'accreditation_page/accreditation_landing.html')
