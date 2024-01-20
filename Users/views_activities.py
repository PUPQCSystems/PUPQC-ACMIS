from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import UpdateForm, CreateUserForm
from Users.models import CustomUser, activity_log
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

@login_required
def admin_activities(request):
    records = activity_log.objects.select_related('acted_by').filter(is_deleted=False).order_by('-datetime_acted')
   
    context = {'records': records}   
    return render(request, 'activity-logs/landing-page.html', context)

def user_activities(request):
    user_id = request.user
    records = activity_log.objects.select_related('CustomUser').filter(acted_by_id = user_id ,is_deleted=False).order_by('-datetime_acted')
   
    context = {'records': records}   
    return render(request, 'activity-logs/landing-page.html', context)
