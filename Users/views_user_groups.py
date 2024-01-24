from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import UpdateForm, CreateUserForm
from Users.models import CustomUser, activity_log
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

@login_required
def landing(request):
 
    return render(request, 'user-groups/main-page/landing-page.html')

