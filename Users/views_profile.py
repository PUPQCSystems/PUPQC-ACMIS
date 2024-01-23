from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import ProfilePicForm, UpdateForm, CreateUserForm
from Users.models import CustomUser, CustomUser_profile, activity_log
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


@login_required
def landing_page(request):
    user = request.user
    profile = CustomUser_profile.objects.filter(account_id=user.id)
    upload_form = ProfilePicForm(request.POST, request.FILES)

    context = { 'user': user, 'profile': profile, 'upload_form':upload_form }


    # Getting all the data inside the Program table and storing it in the context variable
    return render(request, 'user-profile/landing_page.html', context)



@login_required
def upload_profile_pic(request):
    try:
        user_id =  request.user.id
        print('User ID:', user_id)
        user_record= CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, f'Error.. Account Not Found.!') 
        
    # Process the form submission with updated data
    upload_form = ProfilePicForm(request.POST, request.FILES, instance = user_record)   
    if upload_form.is_valid():
        # Save the updated data to the database
        upload_form.instance.modified_by = request.user
        upload_form.save()  

        # Create an instance of the ActivityLog model
        activity_log_entry = activity_log()

        # Set the attributes of the instance
        activity_log_entry.module = "USER PROFILE MODULE"
        activity_log_entry.action = "Uploaded new profile picture"
        activity_log_entry.type = "UPDATE"
        activity_log_entry.datetime_acted =  timezone.now()
        activity_log_entry.acted_by = request.user
        # Set other attributes as needed

        # Save the instance to the database
        activity_log_entry.save()

        # Provide a success message as a JSON response
        messages.success(request, f'Profile picture is successfully uploaded!') 


    else:
        # Return a validation error as a JSON response
        messages.error(request, f'Error.. There might be a problem.!') 

    return redirect('users:profile')



