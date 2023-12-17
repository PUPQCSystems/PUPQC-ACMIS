from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def landing_page(request):
    return render(request, 'accreditation_page/landing_page.html')




