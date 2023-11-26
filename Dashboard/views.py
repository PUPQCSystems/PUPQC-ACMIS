from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def landing_page(request):
  #Getting all the data inside the Program table and storing it to the context variable
    return render(request, 'dashboard_landing/dashboard_landing.html')
