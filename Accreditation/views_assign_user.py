from django.db import IntegrityError
from django.http import JsonResponse
from Users.models import CustomUser, activity_log
from .models import instrument_level_area, instrument_level_folder, user_assigned_to_folder #Import the model for data retieving
from .forms import ChairManAssignedToFolder_Form, CoChairUserAssignedToFolder_Form, MemberAssignedToFolder_Form
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction

@login_required
@permission_required(["Accreditation.add_user_assigned_to_folder", "Accreditation.change_user_assigned_to_folder", "Accreditation.view_user_assigned_to_folder", "Accreditation.delete_user_assigned_to_folder"], raise_exception=True)
def assign_user(request):
    if request.method == "POST":
        chairman_form = ChairManAssignedToFolder_Form(request.POST)
        cochairman_form = CoChairUserAssignedToFolder_Form(request.POST)
        try:
            with transaction.atomic():
                chairman_val = request.POST.get('is_chairman')
                print(chairman_val)
                cochairman_val = request.POST.get('is_cochairman')
                member_list = request.POST.getlist('is_member')
                folder_pk = request.POST.get('folder')
                folder = instrument_level_folder.objects.get(id=folder_pk)
        
                existing_chairman = user_assigned_to_folder.objects.filter(parent_directory=folder, is_chairman=True).first()
                existing_cochairman = user_assigned_to_folder.objects.filter(parent_directory=folder, is_cochairman=True).first()
                existing_members = user_assigned_to_folder.objects.filter(parent_directory=folder, is_member=True)
                existing_assignment = user_assigned_to_folder.objects.filter(parent_directory=folder)

                if existing_assignment:
                    if chairman_val and cochairman_val and cochairman_val != 'None' and existing_chairman and existing_cochairman and existing_members:
                        if existing_chairman.assigned_user_id == int(chairman_val) and existing_cochairman.assigned_user_id == int(cochairman_val) and set(map(int, member_list)) == set(existing_members.values_list('assigned_user_id', flat=True)):
                            return JsonResponse({'error': 'No changes detected. Please make modifications before submission.1'}, status=400)
                        elif existing_chairman.assigned_user_id != int(chairman_val) and existing_cochairman.assigned_user_id != int(cochairman_val) and set(map(int, member_list)) == set(existing_members.values_list('assigned_user_id', flat=True)):
                            existing_chairman.delete()
                            existing_cochairman.delete()
                        
                        elif existing_chairman.assigned_user_id != int(chairman_val) and existing_cochairman.assigned_user_id != int(cochairman_val) and set(map(int, member_list)) != set(existing_members.values_list('assigned_user_id', flat=True)):
                            existing_chairman.delete()
                            existing_cochairman.delete()

                        elif existing_chairman.assigned_user_id != int(chairman_val) and bool(existing_cochairman) == False and int(cochairman_val) and set(map(int, member_list)) != set(existing_members.values_list('assigned_user_id', flat=True)):
                            existing_chairman.delete()
                            existing_cochairman.delete()

                    elif existing_chairman.assigned_user_id != int(chairman_val) and bool(existing_cochairman) == False and cochairman_val :
                            existing_chairman.delete()

                    elif chairman_val and (not cochairman_val or cochairman_val == 'None') and bool(member_list) == False :
                        if existing_chairman.assigned_user_id == int(chairman_val) and bool(existing_members):
                            existing_members.delete()
                            messages.success(request, "Area Managers are successfully assigned!")
                            return JsonResponse({'status': 'success'}, status=200)
                            
                        elif existing_chairman.assigned_user_id == int(chairman_val):
                            return JsonResponse({'error': 'No changes detected. Please make modifications before submission.2'}, status=400)
                        
                    elif chairman_val and (not cochairman_val or cochairman_val == 'None') and bool(member_list) == True :
                        if bool(existing_cochairman):
                            existing_cochairman.delete()
                            messages.success(request, "Co-chairman sucessfully removed!")
                            return JsonResponse({'status': 'success'}, status=200)
                        elif existing_chairman.assigned_user_id == int(chairman_val) and  existing_members and set(map(int, member_list)) == set(existing_members.values_list('assigned_user_id', flat=True)):
                            return JsonResponse({'error': 'No changes detected. Please make modifications before submission.3'}, status=400)
                        
                    
                    elif chairman_val and cochairman_val and cochairman_val != 'None' and existing_chairman and existing_cochairman and bool(member_list) == False:
                        if existing_chairman.assigned_user_id == int(chairman_val):
                            return JsonResponse({'error': 'No changes detected. Please make modifications before submission.4'}, status=400)

                    elif chairman_val and cochairman_val and cochairman_val != 'None' and existing_chairman and bool(existing_cochairman)==False and existing_members:
                        if bool(existing_cochairman)==False:
                             # Save the new co-chairman
                            cochairman = CustomUser.objects.get(id=cochairman_val)
                            cochairman_instance = cochairman_form.save(commit=False)
                            cochairman_instance.assigned_user = cochairman
                            cochairman_instance.area = area
                            cochairman_instance.is_cochairman = True
                            cochairman_instance.assigned_by = request.user
                            cochairman_instance.save()

                if chairman_val is None:
                    return JsonResponse({'error': 'Please select a Chairman for this Area.'}, status=400)
                else:
                    chairman = CustomUser.objects.get(id=int(chairman_val))
                    existing_chairmen = user_assigned_to_folder.objects.filter(parent_directory=folder, is_chairman=True)

                    # Check if there are existing chairmen for the area
                    if existing_chairmen.exists():
                        # If there are existing chairmen, remove them to ensure only one chairman per area
                        existing_chairmen.delete()

                    # Save the new chairman
                    chairman_instance = chairman_form.save(commit=False)
                    chairman_instance.assigned_user = chairman
                    chairman_instance.area = area
                    chairman_instance.is_chairman = True
                    chairman_instance.assigned_by = request.user
                    chairman_instance.save()
                
                if cochairman_val is not None and cochairman_val != 'None':
                    cochairman = CustomUser.objects.get(id=cochairman_val)
                    existing_cochairmen = user_assigned_to_folder.objects.filter(parent_directory=folder, is_cochairman=True)
                    
                    # Check if there are existing co-chairmen for the area
                    if existing_cochairmen.exists():
                        # If there are existing co-chairmen, remove them to ensure only one co-chairman per area
                        existing_cochairmen.delete()
                    
                    # Save the new co-chairman
                    cochairman_instance = cochairman_form.save(commit=False)
                    cochairman_instance.assigned_user = cochairman
                    cochairman_instance.area = area
                    cochairman_instance.is_cochairman = True
                    cochairman_instance.assigned_by = request.user
                    cochairman_instance.save()

                if member_list:
                    if len(member_list) <= 5:
                        member_ids = [int(member_id) for member_id in member_list]  # Convert string IDs to integers
                        conflicting_members = user_assigned_to_folder.objects.filter(parent_directory=folder, is_member=True)
                        if conflicting_members.exists():
                            conflicting_members.delete()
                        
                        for member_id in member_ids:
                            member = CustomUser.objects.get(id=member_id)
                            member_form_instance = MemberAssignedToFolder_Form(request.POST)
                            member_form_instance.instance.assigned_user = member
                            member_form_instance.instance.area = area
                            member_form_instance.instance.is_member = True
                            member_form_instance.instance.assigned_by = request.user
                            member_form_instance.save()
                    else:
                        return JsonResponse({'error': 'The System can only accept up to five (5) members per area.'}, status=400)

            messages.success(request, "Area Managers are successfully assigned!")
            return JsonResponse({'status': 'success'}, status=200)

        except IntegrityError as e:
            return JsonResponse({'error': 'Oops! It seems like you selected a user who is already assigned to this area. Please choose a different user.'}, status=400)