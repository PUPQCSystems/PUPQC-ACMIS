from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import PasswordUpdateForm, UpdateForm, CreateUserForm
from Users.models import CustomUser, auth_group_info
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.contrib import auth
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import random
import string
from django.contrib.auth.hashers import make_password


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
        password_form = PasswordUpdateForm(record, request.POST)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form, created_by, modified_by, password_form))

    context = {'register_form': register_form, 'details': details, 'auth_groups': auth_groups,}   
    return render(request, 'users/landing_page.html', context)


@login_required
def register(request):
    password = generate_mixed_characters(length=12, include_symbols=True)

    form = CreateUserForm(request.POST)

    register_form = CreateUserForm(data={
    'password1': password,
    'password2': password,
    'first_name': request.POST.get('first_name'),
    'last_name': request.POST.get('last_name'),
    'middle_name': request.POST.get('middle_name'),
    'email': request.POST.get('email')
    # ... any other required fields
    })
    auth_group_id = request.POST.get('selected_group')


    if auth_group_id:
        if register_form.is_valid():
            # Example usage:

            print(password) 

            if auth_group_id == 'admin':
                register_form.instance.is_superuser = True

            user_email = request.POST.get('email')
            user_password = password 
            user_first_name = request.POST.get('first_name')
            user_last_name = request.POST.get('last_name')


            template = render_to_string('email-templates/register-email.html', 
                                        {'email': user_email, 'password': user_password, 'first_name': user_first_name, 'last_name': user_last_name})

            if auth_group_id == 'admin':
                register_form.instance.is_superuser = True
                register_form.instance.created_by = request.user
                register_form.instance.password = make_password(password)
                user_record = register_form.save()


            else:                # Create a new group
                register_form.instance.created_by = request.user
                register_form.instance.password = make_password(password)
                user_record = register_form.save()

                user_id = user_record.id
                group = Group.objects.get(id=auth_group_id)
                # Add a user to the group
                user = CustomUser.objects.get(id=user_id)
                user.groups.add(group)

   

  

            email = EmailMessage(
                'Welcome to the Accreditation and Certification Management Information System!',
                template,
                settings.EMAIL_HOST_USER,
                [user_email],
            )


            email.fail_silently=False
            # Send the email
            email.send()
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
        password_form = PasswordUpdateForm(account, request.POST)

        if update_form.is_valid():
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            user_email = request.POST.get('email')
            user_first_name = request.POST.get('first_name')
            user_last_name = request.POST.get('last_name')
            user_middle_name = request.POST.get('middle_name')

            #------------------------[ SAVING THE DATA IF THERE IS A VALUE TO THE PASSWORD FIELDS ]------------------------
            if new_password1 or new_password2:
                if password_form.is_valid():
                    auth_group_id = request.POST.get('selected_group')

                    if auth_group_id:

                        if auth_group_id == 'admin':
                            update_form.instance.is_superuser = True
                            user_role = 'System Admin'

                        else:
                            # Assuming you have a user instance and a group instance
                            group = Group.objects.get(pk=auth_group_id)  # Replace new_group_id with the desired group ID
                            user_role = group.name
                            # Clear existing groups and set the new group
                            account.groups.set([group])
                            # Save the updated data to the database

                        template = render_to_string('email-templates/update-account-email.html', 
                                            {'email': user_email
                                             , 'password': new_password1
                                             , 'first_name': user_first_name
                                             , 'last_name': user_last_name
                                             , 'middle_name': user_middle_name
                                             , 'role': user_role})
                        

                        # Save the updated data to the database
                        update_form.instance.modified_by = request.user
                        update_form.save()
                        password_form.save()

                        #Codes for sending Email to the user's account email 
                        email = EmailMessage(
                            'Welcome to the Accreditation and Certification Management Information System!',
                            template,
                            settings.EMAIL_HOST_USER,
                            [user_email],
                        )
                        email.fail_silently=False
                        # Send the email
                        email.send()

                        # Provide a success message as a JSON response
                        messages.success(request, f'The account is successfully updated!') 
                        url_landing = "/user/"
                        return JsonResponse({'url_landing': url_landing}, status=200)
                    else:
                        # Return a validation error using a JSON response
                        return JsonResponse({'error': 'Please make sure that you assigned a Role to the user account before submitting the form.'}, status=400)

                else:
                    # Return a validation error as a JSON response
                    return JsonResponse({'errors': password_form.errors}, status=400)
                

            # ------------------------[ SAVING THE DATE IF THERE IS NO VALUE IN THE PASSWORD FIELD ]------------------------
            else:
                auth_group_id = request.POST.get('selected_group')
                if auth_group_id:

                    if auth_group_id == 'admin':
                        update_form.instance.is_superuser = True
                        user_role = 'System Admin'

                    else:
                        # Assuming you have a user instance and a group instance
                        group = Group.objects.get(pk=auth_group_id)  # Replace new_group_id with the desired group ID
                        user_role = group.name
                        # Clear existing groups and set the new group
                        account.groups.set([group])
                        # Save the updated data to the database
                    update_form.instance.modified_by = request.user
                    update_form.save()

                    template = render_to_string('email-templates/update-account-email.html', 
                                            {   'email': user_email
                                                , 'password': False
                                                , 'first_name': user_first_name
                                                , 'last_name': user_last_name
                                                , 'middle_name': user_middle_name
                                                , 'role': user_role
                                             })
                    



                    #Codes for sending Email to the user's account email 
                    email = EmailMessage(
                        'Welcome to the Accreditation and Certification Management Information System!',
                        template,
                        settings.EMAIL_HOST_USER,
                        [user_email],
                    )
                    email.fail_silently=False
                    # Send the email
                    email.send()

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



@login_required
def logout_view(request):
  auth.logout(request)
  # Redirect to a success page.
  return HttpResponseRedirect("/accounts/login/")


def generate_mixed_characters(length=10, 
                              include_lowercase=True, 
                              include_uppercase=True, 
                              include_digits=True, 
                              include_symbols=False):
    """
    Generates a string of mixed characters with specified options.

    Args:
        length: Desired length of the generated string (default: 10)
        include_lowercase: Whether to include lowercase letters (default: True)
        include_uppercase: Whether to include uppercase letters (default: True)
        include_digits: Whether to include digits (default: True)
        include_symbols: Whether to include special symbols (default: False)
    """

    character_set = ""
    if include_lowercase:
        character_set += string.ascii_lowercase
    if include_uppercase:
        character_set += string.ascii_uppercase
    if include_digits:
        character_set += string.digits
    if include_symbols:
        character_set += string.punctuation

    return ''.join(random.choice(character_set) for _ in range(length))



