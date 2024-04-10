from django.db import IntegrityError
from django.http import JsonResponse
from Accreditation.models_views import UserGroupView
from Users.models import CustomUser, activity_log
from .models import instrument_level_folder, user_assigned_to_folder #Import the model for data retieving
from .forms import ChairManAssignedToFolder_Form, CoChairUserAssignedToFolder_Form, MemberAssignedToFolder_Form
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render, redirect

@login_required
@permission_required(["Accreditation.add_user_assigned_to_folder", "Accreditation.change_user_assigned_to_folder", "Accreditation.view_user_assigned_to_folder", "Accreditation.delete_user_assigned_to_folder"], raise_exception=True)
def assign_user(request):
    if request.method == "POST":
        list_of_users = request.POST.getlist('assigned-user')
        assigned_role = request.POST.get('assign-selected-role')
        message = request.POST.get('message')
        folder_id = request.POST.get('folder-id')
        is_child = request.POST.get('is-child')
        max_member = 8
        max_chairman = 1
        max_cochairman= 1
        email_subject = "You've Been Assigned to a Folder"
        folder_record = instrument_level_folder.objects.get(id=folder_id)
        existing_chairman = user_assigned_to_folder.objects.filter(parent_directory_id=folder_id, is_chairman=True).exists()
        existing_cochairman = user_assigned_to_folder.objects.filter(parent_directory_id=folder_id, is_cochairman=True).exists()
        existing_members = user_assigned_to_folder.objects.filter(parent_directory_id=folder_id, is_member=True).count()


        print(list_of_users)
        # ------------------------[ START OF ERROR HANDLING CODES ]------------------------# 
        if len(list_of_users) == 0:
          return JsonResponse({'error': 'Please make sure to select a user before submitting the form.'}, status=400)
        


        elif assigned_role == 'chairman':
            if existing_chairman:
                return JsonResponse({'error': 'There is a user who is already assigned as a chairman to this folder.'}, status=400)
            
            elif len(list_of_users) > max_chairman:
                return JsonResponse({'error': 'There can only be a maximum of one chairman to the folder.'}, status=400)
            else:
                # If there is no error, then this code will be executed by the machine
                if list_of_users:
                # The list_of_persmission variable is a list so we use for loop to get the permission individually
                    for user_id in list_of_users:
                    # Code to save the records. This will create a new record in the auth_group_permissions table
                        user_assigned_to_folder.objects.create(
                            parent_directory_id = folder_id,
                            assigned_by = request.user,
                            assigned_user_id = user_id,
                            is_chairman = True
                        )

                        user_record= CustomUser.objects.get(id=user_id)
                        user_email = user_record.email
                        template = render_to_string('email-templates/assign-user-email.html', 
                                                                {   'first_name': user_record.first_name
                                                                    , 'last_name': user_record.last_name
                                                                    , 'role': 'Chairman'
                                                                    , 'folder_name': folder_record.name
                                                                 })
                        
                        email = EmailMessage(
                            email_subject,
                            template,
                            settings.EMAIL_HOST_USER,
                            [user_email],
                        )


                        email.fail_silently=False
                        # Send the email
                        email.send()
                        record = instrument_level_folder.objects.get(id=folder_id) #Getting all the data inside the Program table and storing it to the context variable
                        user_records = UserGroupView.objects.all()
                        assigned_users = user_assigned_to_folder.objects.select_related('assigned_user').filter(parent_directory_id=folder_id)
                        assigned_user_ids = user_assigned_to_folder.objects.filter(parent_directory_id=folder_id).values_list('assigned_user_id', flat=True)
                        users_not_assigned = user_records.exclude(id__in=assigned_user_ids)
                        context={ 'assigned_users': assigned_users
                                    , 'user_not_assigned': users_not_assigned
                                    , 'record': record }
                        
                        if is_child:
                            return render(request, 'accreditation-level-child-directory/main-page/partials/assign-modal-user-list.html', context)

                        else:
                            return render(request, 'accreditation-level-parent-directory/main-page/partials/assign-modal-user-list.html', context)


                else:
                    # Return a validation error using a JSON response
                    return JsonResponse({'error': 'Please make sure to select a user before submitting the form.'}, status=400)
            
        elif assigned_role == 'member':
            if existing_members == max_member:
                return JsonResponse({'error': "Can't assign new members because the folder already reached its maximum number of member."}, status=400)
            
            elif existing_members < max_member:
                members_count_left = max_member - existing_members
                if len(list_of_users) > members_count_left:
                    return JsonResponse({'error': f"Can't assign new members. You selected {len(list_of_users)} users, but it only accept {members_count_left} users."}, status=400)

                else:
                        # If there is no error, then this code will be executed by the machine
                    if list_of_users:
                    # The list_of_persmission variable is a list so we use for loop to get the permission individually
                        for user_id in list_of_users:
                        # Code to save the records. This will create a new record in the auth_group_permissions table
                            user_assigned_to_folder.objects.create(
                                parent_directory_id = folder_id,
                                assigned_by = request.user,
                                assigned_user_id = user_id,
                                is_member = True
                            )
                            user_record= CustomUser.objects.get(id=user_id)
                            user_email = user_record.email
                            template = render_to_string('email-templates/assign-user-email.html', 
                                                                    {   'first_name': user_record.first_name
                                                                        , 'last_name': user_record.last_name
                                                                        , 'role': 'Member'
                                                                        , 'folder_name': folder_record.name
                                                                    })

                            email = EmailMessage(
                                email_subject,
                                template,
                                settings.EMAIL_HOST_USER,
                                [user_email],
                            )


                            email.fail_silently=False
                            # Send the email
    
                            email.send()

                        record = instrument_level_folder.objects.get(id=folder_id) #Getting all the data inside the Program table and storing it to the context variable
                        user_records = UserGroupView.objects.all()
                        assigned_users = user_assigned_to_folder.objects.select_related('assigned_user').filter(parent_directory_id=folder_id)
                        assigned_user_ids = user_assigned_to_folder.objects.filter(parent_directory_id=folder_id).values_list('assigned_user_id', flat=True)
                        users_not_assigned = user_records.exclude(id__in=assigned_user_ids)
                        context={ 'assigned_users': assigned_users
                                    , 'user_not_assigned': users_not_assigned
                                    , 'record': record }
                        if is_child:
                            return render(request, 'accreditation-level-child-directory/main-page/partials/assign-modal-user-list.html', context)

                        else:
                            return render(request, 'accreditation-level-parent-directory/main-page/partials/assign-modal-user-list.html', context)
                    


                    else:
                        # Return a validation error using a JSON response
                        return JsonResponse({'error': 'Please make sure to select a user before submitting the form.'}, status=400)
                

            elif len(list_of_users) > max_member:
                return JsonResponse({'error': 'There can only be a maximun of eight member to the folder.'}, status=400)
            

        elif assigned_role == 'co-chairman':
            if existing_cochairman:
                return JsonResponse({'error': 'There is a user who is already assigned as a co-chairman to this folder.'}, status=400)
            
            elif len(list_of_users) > max_cochairman:
                return JsonResponse({'error': 'There can only be a maximum of one co-chairman to the folder.'}, status=400)
            
            else:
                  # If there is no error, then this code will be executed by the machine
                if list_of_users:
                # The list_of_persmission variable is a list so we use for loop to get the permission individually
                    for user_id in list_of_users:
                    # Code to save the records. This will create a new record in the auth_group_permissions table
                        user_assigned_to_folder.objects.create(
                            parent_directory_id = folder_id,
                            assigned_by = request.user,
                            assigned_user_id = user_id,
                            is_cochairman = True
                        )

                        user_record= CustomUser.objects.get(id=user_id)
                        user_email = user_record.email
                        template = render_to_string('email-templates/assign-user-email.html', 
                                                                {   'first_name': user_record.first_name
                                                                    , 'last_name': user_record.last_name
                                                                    , 'role': 'Co-chairman'
                                                                    , 'folder_name': folder_record.name
                                                                 })
                        
                        email = EmailMessage(
                            email_subject,
                            template,
                            settings.EMAIL_HOST_USER,
                            [user_email],
                        )


                        email.fail_silently=False
                        # Send the email
                        email.send()
                        record = instrument_level_folder.objects.get(id=folder_id) #Getting all the data inside the Program table and storing it to the context variable
                        user_records = UserGroupView.objects.all()
                        assigned_users = user_assigned_to_folder.objects.select_related('assigned_user').filter(parent_directory_id=folder_id)
                        assigned_user_ids = user_assigned_to_folder.objects.filter(parent_directory_id=folder_id).values_list('assigned_user_id', flat=True)
                        users_not_assigned = user_records.exclude(id__in=assigned_user_ids)
                        context={ 'assigned_users': assigned_users
                                    , 'user_not_assigned': users_not_assigned
                                    , 'record': record }
                        if is_child:
                            return render(request, 'accreditation-level-child-directory/main-page/partials/assign-modal-user-list.html', context)

                        else:
                            return render(request, 'accreditation-level-parent-directory/main-page/partials/assign-modal-user-list.html', context)

                        


                else:
                    # Return a validation error using a JSON response
                    return JsonResponse({'error': 'Please make sure to select a user before submitting the form.'}, status=400)
            
        # ------------------------[ END OF ERROR HANDLING CODES ]------------------------# 
            

def change_to_chairman(request, pk, folder_pk):
    # Check if the chairman is existing 

    if request.method == 'POST':    
        email_subject = "You've Been Assigned to a Folder"
        folder_record = instrument_level_folder.objects.get(id=folder_pk)
        existing_chairman = user_assigned_to_folder.objects.filter(parent_directory_id=folder_pk, is_chairman=True).exists()
        already_chairman = user_assigned_to_folder.objects.filter(parent_directory_id=folder_pk, is_chairman=True, assigned_user_id=pk).exists()
        is_assigned = user_assigned_to_folder.objects.filter(parent_directory_id=folder_pk, assigned_user_id=pk)

        if existing_chairman:
            return JsonResponse({'error': 'There is a user who is already assigned as a chairman to this folder.'}, status=400)
        
        elif already_chairman:
            return JsonResponse({'error': 'The user is already assigned as a chairman to this folder.'}, status=400)
        
        else:

            if is_assigned:
                is_assigned.delete()

            user_record = CustomUser.objects.get(id=pk)
            # Code to save the records. This will create a new record in the auth_group_permissions table
            user_assigned_to_folder.objects.create(
                parent_directory_id = folder_pk,
                assigned_by = request.user,
                assigned_user_id = pk,
                is_chairman = True
            )

    
            user_email = user_record.email
            template = render_to_string('email-templates/assign-user-edit-email.html', 
                                                    {   'first_name': user_record.first_name
                                                        , 'last_name': user_record.last_name
                                                        , 'role': 'Chairman'
                                                        , 'folder_name': folder_record.name
                                                        })
            
            email = EmailMessage(
                email_subject,
                template,
                settings.EMAIL_HOST_USER,
                [user_email],
            )


            email.fail_silently=False
            # Send the email
            email.send()
            record = instrument_level_folder.objects.get(id=folder_pk) #Getting all the data inside the Program table and storing it to the context variable
            user_records = UserGroupView.objects.all()
            assigned_users = user_assigned_to_folder.objects.select_related('assigned_user').filter(parent_directory_id=folder_pk)
            assigned_user_ids = user_assigned_to_folder.objects.filter(parent_directory_id=folder_pk).values_list('assigned_user_id', flat=True)
            users_not_assigned = user_records.exclude(id__in=assigned_user_ids)
            context={ 'assigned_users': assigned_users
                     , 'user_not_assigned': users_not_assigned
                      , 'record': record }
            
            is_child = request.POST.get('is-child')
            if is_child:
                return render(request, 'accreditation-level-child-directory/main-page/partials/assign-modal-user-list.html', context)

            else:
                return render(request, 'accreditation-level-parent-directory/main-page/partials/assign-modal-user-list.html', context)

        



def change_to_member(request, pk, folder_pk):
    # Check if the chairman is existing 
    max_member = 8
    email_subject = "You've Been Assigned to a Folder"
    folder_record = instrument_level_folder.objects.get(id=folder_pk)
    existing_members = user_assigned_to_folder.objects.filter(parent_directory_id=folder_pk, is_member=True).count()
    already_member = user_assigned_to_folder.objects.filter(parent_directory_id=folder_pk, is_member=True, assigned_user_id=pk).exists()
    is_assigned = user_assigned_to_folder.objects.filter(parent_directory_id=folder_pk, assigned_user_id=pk)

    if existing_members == max_member:
        return JsonResponse({'error': "Can't assign new members because the folder already reached its maximum number of member."}, status=400)
    
    elif existing_members < max_member:
        members_count_left = max_member - existing_members
        if members_count_left >= 1:
            if is_assigned:
                is_assigned.delete()
            # Code to save the records. This will create a new record in the auth_group_permissions table
            user_assigned_to_folder.objects.create(
                parent_directory_id = folder_pk,
                assigned_by = request.user,
                assigned_user_id = pk,
                is_member = True
            )

            user_record = CustomUser.objects.get(id=pk)
            user_email = user_record.email
            template = render_to_string('email-templates/assign-user-edit-email.html', 
                                                    {   'first_name': user_record.first_name
                                                        , 'last_name': user_record.last_name
                                                        , 'role': 'Member'
                                                        , 'folder_name': folder_record.name
                                                        })
            
            email = EmailMessage(
                email_subject,
                template,
                settings.EMAIL_HOST_USER,
                [user_email],
            )


            email.fail_silently=False
            # Send the email
            email.send()
            record = instrument_level_folder.objects.get(id=folder_pk) #Getting all the data inside the Program table and storing it to the context variable
            user_records = UserGroupView.objects.all()
            assigned_users = user_assigned_to_folder.objects.select_related('assigned_user').filter(parent_directory_id=folder_pk)
            assigned_user_ids = user_assigned_to_folder.objects.filter(parent_directory_id=folder_pk).values_list('assigned_user_id', flat=True)
            users_not_assigned = user_records.exclude(id__in=assigned_user_ids)
            context={ 'assigned_users': assigned_users
                     , 'user_not_assigned': users_not_assigned
                      , 'record': record }
            is_child = request.POST.get('is-child')
            if is_child:
                return render(request, 'accreditation-level-child-directory/main-page/partials/assign-modal-user-list.html', context)

            else:
                return render(request, 'accreditation-level-parent-directory/main-page/partials/assign-modal-user-list.html', context)

    elif already_member:
        return JsonResponse({'error': 'The user is already assigned as a member to this folder.'}, status=400)
    


def change_to_cochariman(request, pk, folder_pk):
        # Check if the chairman is existing 
    email_subject = "You've Been Assigned to a Folder"
    folder_record = instrument_level_folder.objects.get(id=folder_pk)
    existing_cochairman = user_assigned_to_folder.objects.filter(parent_directory_id=folder_pk, is_cochairman=True).exists()
    is_assigned = user_assigned_to_folder.objects.filter(parent_directory_id=folder_pk, assigned_user_id=pk)
    already_cochairman = user_assigned_to_folder.objects.filter(parent_directory_id=folder_pk, is_cochairman=True, assigned_user_id=pk).exists()

    if existing_cochairman:
        return JsonResponse({'error': 'There is a user who is already assigned as a co-chairman to this folder.'}, status=400)
    
    elif already_cochairman:
        return JsonResponse({'error': 'The user is already assigned as a co-chairman to this folder.'}, status=400)
    
    else:
        # Code to save the records. This will create a new record in the auth_group_permissions table

        if is_assigned:
            is_assigned.delete()
        user_record = CustomUser.objects.get(id=pk)
        user_assigned_to_folder.objects.create(
            parent_directory_id = folder_pk,
            assigned_by = request.user,
            assigned_user_id = user_record.id,
            is_cochairman = True
        )
        user_email = user_record.email
        template = render_to_string('email-templates/assign-user-edit-email.html', 
                                                {   'first_name': user_record.first_name
                                                    , 'last_name': user_record.last_name
                                                    , 'role': 'Co-chairman'
                                                    , 'folder_name': folder_record.name
                                                    })
        
        email = EmailMessage(
            email_subject,
            template,
            settings.EMAIL_HOST_USER,
            [user_email],
        )


        email.fail_silently=False
        # Send the email
        email.send()
        record = instrument_level_folder.objects.get(id=folder_pk) #Getting all the data inside the Program table and storing it to the context variable
        user_records = UserGroupView.objects.all()
        assigned_users = user_assigned_to_folder.objects.select_related('assigned_user').filter(parent_directory_id=folder_pk)
        assigned_user_ids = user_assigned_to_folder.objects.filter(parent_directory_id=folder_pk).values_list('assigned_user_id', flat=True)
        users_not_assigned = user_records.exclude(id__in=assigned_user_ids)
        context={ 'assigned_users': assigned_users
                    , 'user_not_assigned': users_not_assigned
                    , 'record': record }
                    
        is_child = request.POST.get('is-child')
        if is_child:
            return render(request, 'accreditation-level-child-directory/main-page/partials/assign-modal-user-list.html', context)

        else:
            return render(request, 'accreditation-level-parent-directory/main-page/partials/assign-modal-user-list.html', context)
    
def removed_user_to_folder(request, pk, folder_pk):
    assigned_user_record = user_assigned_to_folder.objects.get(parent_directory_id=folder_pk, assigned_user_id=pk)
    assigned_user_record.delete()

    record = instrument_level_folder.objects.get(id=folder_pk) #Getting all the data inside the Program table and storing it to the context variable
    user_records = UserGroupView.objects.all()
    assigned_users = user_assigned_to_folder.objects.select_related('assigned_user').filter(parent_directory_id=folder_pk)
    assigned_user_ids = user_assigned_to_folder.objects.filter(parent_directory_id=folder_pk).values_list('assigned_user_id', flat=True)
    users_not_assigned = user_records.exclude(id__in=assigned_user_ids)
    context={ 'assigned_users': assigned_users
                , 'user_not_assigned': users_not_assigned
                , 'record': record }
    is_child = request.POST.get('is-child')
    if is_child:
        return render(request, 'accreditation-level-child-directory/main-page/partials/assign-modal-user-list.html', context)

    else:
        return render(request, 'accreditation-level-parent-directory/main-page/partials/assign-modal-user-list.html', context)

