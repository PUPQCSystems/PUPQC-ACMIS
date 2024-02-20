from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from .forms import AuthGroup_Form, UpdateForm, CreateUserForm
from Users.models import CustomUser, activity_log, auth_group_info
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group, Permission

from django.contrib.contenttypes.models import ContentType
# import User model
from Users.models import CustomUser 
 


@login_required
def landing(request):
    groups_info = auth_group_info.objects.select_related('auth_group').filter(is_deleted=False)
    context = {
    'records': groups_info
    }

    return render(request, 'user-groups/main-page/landing-page.html', context)


class CreateUserGroups(View):
    def get(self, request, *args, **kwargs):

        group_form = AuthGroup_Form(request.POST or None)

            
            # Add permissions to the group
        view_permission = Permission.objects.all()
        context = {
            'permissions': view_permission,
            'group_form': group_form,
        }
        return render(request, 'user-groups/main-page/create-page.html', context)
    
    def post(self, request, *args, **kwargs):
        
        group_form = AuthGroup_Form(request.POST or None)
          #This code contains the lists of id of the chosen permissions
        list_of_persmission = request.POST.getlist('selected_permissions')

        if list_of_persmission:
            if group_form.is_valid():
                group_name = request.POST.get('name')
                new_group, created = Group.objects.get_or_create(name = group_name)
                group_id = new_group.id
            
                 # Create an instance of the ActivityLog model
                activity_log_entry = activity_log()

                # Set the attributes of the instance
                activity_log_entry.module = "USER GROUP MODULE"
                activity_log_entry.action = "Created a record"
                activity_log_entry.type = "CREATE"
                activity_log_entry.datetime_acted =  timezone.now()
                activity_log_entry.acted_by = request.user
                # Set other attributes as needed
                # Save the instance to the database
                activity_log_entry.save()

                # Create an instance of the Auth Group Info model
                group_info = auth_group_info()
                # Set the attributes of the instance
                group_info.auth_group_id = group_id
                group_info.created_at =  timezone.now()
                group_info.created_by = request.user
                group_info.is_deleted = False
                # Set other attributes as needed
                # Save the instance to the database
                group_info.save()

            

                # The list_of_persmission variable is a list so we use for loop to get the permission individually
                for permission in list_of_persmission:
                # Code to save the records. This will create a new record in the auth_group_permissions table
                    print('The permission id:', permission)
                    new_group.permissions.add(permission)
                
                redirect_url = '/user/groups/'
                messages.success(request, f' The User Group is successfully created!') 
                return JsonResponse({'status': 'success', 'redirect_url': redirect_url}, status=200)

            else:
                # Return a validation error using a JSON response
                return JsonResponse({'errors': group_form.errors}, status=400)


        else:
            # Return a validation error using a JSON response
            return JsonResponse({'error': 'Please make sure to select a permission before submitting the form.'}, status=400)

@login_required
def archive(request, pk):
    # Gets the records who have this ID
    group_info = auth_group_info.objects.get(id=pk)

    #After getting that record, this code will delete it.
    group_info.modified_by = request.user
    group_info.is_deleted=True
    group_info.deleted_at = timezone.now()
    group_info.save()

 # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "USER GROUP MODULE"
    activity_log_entry.action = "Archived a record"
    activity_log_entry.type = "ARCHIVE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'User Group is successfully archived!') 
    return redirect('users:user-groups')

#------------------------------------------------------------[ ARCHIVE PAGE CODES ]------------------------------------------------------------#
@login_required
def archive_landing(request):
    groups_info = auth_group_info.objects.select_related('auth_group').filter(is_deleted=True)
    context = {
    'records': groups_info
    }

    return render(request, 'user-groups/archive-page/landing-page.html', context)

@login_required
def restore(request, pk):
    # Gets the records who have this ID
    group_info = auth_group_info.objects.get(id=pk)

    #After getting that record, this code will restore it.
    group_info.modified_by = request.user
    group_info.deleted_at = None
    group_info.is_deleted=False
    group_info.save()

  # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "USER GROUP MODULE"
    activity_log_entry.action = "Restored a record"
    activity_log_entry.type = "RESTORE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'User Group is successfully restored!') 
    return redirect('users:user-groups-archive-page')

@login_required
def destroy(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                group_info = auth_group_info.objects.get(id=pk)
                auth_group_id = group_info.auth_group_id
                auth_group = Group.objects.get(id=auth_group_id)

                #After getting that record, this code will delete it.
                group_info.delete()
                auth_group.delete()

                # Create an instance of the ActivityLog model
                activity_log_entry = activity_log()

                # Set the attributes of the instance
                activity_log_entry.module = "USER GROUP MODULE"
                activity_log_entry.action = "Permanently deleted a record"
                activity_log_entry.type = "DESTROY"
                activity_log_entry.datetime_acted =  timezone.now()
                activity_log_entry.acted_by = request.user
                # Set other attributes as needed

                # Save the instance to the database
                activity_log_entry.save()

                messages.success(request, f'Auth Group is permanently deleted!') 
                return JsonResponse({'success': True}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})
