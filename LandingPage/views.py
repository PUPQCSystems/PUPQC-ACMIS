from django.contrib import messages
from django.shortcuts import redirect, render


def index_page(request):
    return render(request, 'index-page/index.html')

def about_page(request):
    return render(request, 'about/about.html')