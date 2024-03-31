from django.db import IntegrityError
from django.http import JsonResponse
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

@login_required
@permission_required(["Accreditation.add_user_assigned_to_folder", "Accreditation.change_user_assigned_to_folder", "Accreditation.view_user_assigned_to_folder", "Accreditation.delete_user_assigned_to_folder"], raise_exception=True)
def assign_user(request):
    if request.method == "POST":
        list_of_users = request.POST.getlist('assigned-user')
        assigned_role = request.POST.get('assign-selected-role')
        message = request.POST.get('message')
        folder_id = request.POST.get('folder-id')
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
                    messages.success(request, 'The selected members are sucessfully assigned to the folder.')
                    return JsonResponse({'success': True}, status=200)


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

                        messages.success(request, 'The selected members are sucessfully assigned to the folder.')
                        return JsonResponse({'success': True}, status=200)
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
                    messages.success(request, 'The selected members are sucessfully assigned to the folder.')
                    return JsonResponse({'success': True}, status=200)

                        


                else:
                    # Return a validation error using a JSON response
                    return JsonResponse({'error': 'Please make sure to select a user before submitting the form.'}, status=400)
            
        # ------------------------[ END OF ERROR HANDLING CODES ]------------------------# 
            

            