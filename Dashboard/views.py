from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from .forms import CreateForm
from django.contrib import messages

# Create your views here.
def landing_page(request):
  #Getting all the data inside the Program table and storing it to the context variable
    return render(request, 'dashboard_landing/dashboard_landing.html')