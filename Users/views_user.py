from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import UpdateForm, CreateUserForm
from Users.models import CustomUser, auth_group_info
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission

@login_required
def landing_page(request):
    # Getting all the data inside the Program table and storing it in the context variable
    register_form = CreateUserForm()
    records = CustomUser.objects.filter(deactivated_at=None, is_active=True)
    auth_groups = auth_group_info.objects.select_related('auth_group').filter(is_deleted=False)

    # Initialize an empty list to store update forms for each record
    details = []

    # Iterate through each record and create an update form for it
    for record in records:
        update_form = UpdateForm(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form, created_by, modified_by))

    context = {'register_form': register_form, 'details': details, 'auth_groups': auth_groups}   
    return render(request, 'users/landing_page.html', context)


@login_required
def register(request):
    register_form = CreateUserForm(request.POST)
    auth_group_id = request.POST.get('selected_group')

    if auth_group_id:
        if register_form.is_valid():
            # Create a new group
            group = Group.objects.get(id=auth_group_id)
            register_form.instance.created_by = request.user
            user_record = register_form.save()
            user_id = user_record.id

            # Add a user to the group
            user = CustomUser.objects.get(id=user_id)
            user.groups.add(group)

            messages.success(request, 'Account was successfully created.')
            return JsonResponse({'success': True}, status=200)
        
        else:
            # Return a validation error using a JSON response
            return JsonResponse({'errors': register_form.errors}, status=400)
    else:
        # Return a validation error using a JSON response
        return JsonResponse({'error': 'Please make sure that you assigned a Role to the user account before submitting the form.'}, status=400)

    
    #This is the function for updating the record
@login_required
def update_account(request, pk):
    # Retrieve the program object with the given primary key (pk)
    try:
        account = CustomUser.objects.get(id=pk)
        first_name = account.first_name
    except CustomUser.DoesNotExist:
        return JsonResponse({'errors': 'User not found'}, status=404)

    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = UpdateForm(request.POST or None, instance=account)

        if update_form.is_valid():
            auth_group_id = request.POST.get('selected_group')

            if auth_group_id:
              # Assuming you have a user instance and a group instance
                group = Group.objects.get(pk=auth_group_id)  # Replace new_group_id with the desired group ID

                # Clear existing groups and set the new group
                account.groups.set([group])
                # Save the updated data to the database
                update_form.instance.modified_by = request.user
                update_form.save()
                email = update_form.cleaned_data.get('email')

                # Provide a success message as a JSON response
                messages.success(request, f'The account is successfully updated!') 
                url_landing = "/user/"
                return JsonResponse({'url_landing': url_landing}, status=200)
            else:
                # Return a validation error using a JSON response
                return JsonResponse({'error': 'Please make sure that you assigned a Role to the user account before submitting the form.'}, status=400)

        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)

        
@login_required
def deactivate_account(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                account = CustomUser.objects.get(id=pk)

                #After getting that record, this code will deactivate it.
                account.modified_by = request.user
                account.deactivated_at = timezone.now()
                account.is_active = False
                account.save()
                messages.success(request, f'The Account is successfully deactivated!') 
                url_landing = "/user/"
                return JsonResponse({'success': True, 'url_landing': url_landing}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})




    #After getting that record, this code will delete it.

    return redirect('programs:landing')

        

#----------------------------------------[ ARCHIVE PAGE FUNCTIONS ]----------------------------------------#
@login_required
def archive_landing(request):
    # Getting all the data inside the Program table and storing it in the context variable

    records = CustomUser.objects.filter(is_active=False)

    # Initialize an empty list to store update forms for each record
    details = []

    # Iterate through each record and create an update form for it
    for record in records:
        update_form = UpdateForm(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record,  update_form, created_by, modified_by))

    context = {'details': details}   
    return render(request, 'deactivated-users/landing_page.html', context)

@login_required
def reactivate_account(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                account = CustomUser.objects.get(id=pk)

                #After getting that record, this code will restore it.
                account.modified_by = request.user
                account.is_active = True
                account.deactivated_at = None
                account.save()

                messages.success(request, f'The account is successfully reactivated!') 
                url_landing = "/user/archive_page/"
                return JsonResponse({'success': True, 'url_landing': url_landing}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})




