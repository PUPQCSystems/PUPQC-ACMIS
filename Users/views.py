from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def users(request):
    form = UserCreationForm()
    return render(request,  'users/landing_page.html', {'form': form})