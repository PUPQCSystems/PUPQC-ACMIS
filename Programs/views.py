from django.shortcuts import render
from django.http import HttpResponse
from .models import Program

# Create your views here.


def landing_page(request):
    context = { 'records': Program.objects.all() } 
    return render(request, 'landing_page/landing_page.html', context)
