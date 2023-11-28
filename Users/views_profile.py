from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import UpdateForm, CreateUserForm
from Users.models import CustomUser, CustomUser_profile
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

@login_required
def landing_page(request):
    user = request.user
    profile = CustomUser_profile.objects.filter(account_id=user.id)

    context = { 'user': user, 'profile': profile }

    print(profile.religion)

    # Getting all the data inside the Program table and storing it in the context variable
    return render(request, 'user-profile/landing_page.html', context)
