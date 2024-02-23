from django.db import IntegrityError
from django.utils import timezone
from django.views import View
from rest_framework import generics, viewsets, status
from django.shortcuts import render, redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import Group, Permission
from Accreditation.models_views import UserGroupView
from Users.models import CustomUser, activity_log
from .models import instrument, instrument_level, instrument_level_area, program_accreditation, user_assigned_to_area #Import the model for data retieving
from Accreditation.serializers import InstrumentSerializer
from .forms import ChairManAssignedToArea_Form, CoChairUserAssignedToArea_Form, Create_Instrument_Form, Create_InstrumentLevel_Form, Create_LevelArea_Form, LevelAreaFormSet, MemberAssignedToArea_Form
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.db import connection
from django.db import transaction

@login_required
@permission_required("Accreditation.view_instrument_level_area", raise_exception=True)
def landing_page(request, pk, accred_pk):
    chairman_form =ChairManAssignedToArea_Form(request.POST or None)
    cochairman_form = CoChairUserAssignedToArea_Form(request.POST or None)
    member_form = MemberAssignedToArea_Form(request.POST or None)
    formset  = LevelAreaFormSet(queryset=instrument_level_area.objects.none())
    # records = instrument_level_area.objects.select_related('instrument_level','area').filter(instrument_level=pk, is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable
    records = instrument_level_area.objects.select_related('instrument_level', 'area').filter(instrument_level=pk, is_deleted=False)


    accred_program = program_accreditation.objects.select_related('instrument_level', 'program').get(id=accred_pk)
    user_records = UserGroupView.objects.all()
    # group = Group.objects.get(id=auth_group_id)

    # Initialize an empty list to store update forms for each record
    details = []

    # Iterate through each record and create an update form for it
    for record in records:
        user_counts = user_assigned_to_area.objects.filter(area_id=record.id).count()
        assigned_user = user_assigned_to_area.objects.filter(area_id=record.id).values_list('assigned_user_id', 'area_id', 'is_chairman', 'is_cochairman', 'is_member')
        print(assigned_user)
        update_form = Create_LevelArea_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, user_counts, assigned_user ,update_form, created_by, modified_by))

    context = { 'records': records,
                'details': details, 
                'pk': pk,   
                'area_formset': formset, 
                'user_records': user_records,
                'accred_program': accred_program,
                'chairman_form': chairman_form,
                'cochairman_form': cochairman_form,
                'member_form': member_form
                }  #Getting all the data inside the type table and storing it to the context variable

    return render(request, 'accreditation-page/instrument-area/main-page/landing-page.html', context)

@login_required
@permission_required("Accreditation.delete_instrument_level_area", raise_exception=True)
def archive(request, ins_pk, pk):
    # Gets the records who have this ID
    level_area = instrument_level_area.objects.get(id=pk)

    #After getting that record, this code will delete it.
    level_area.modified_by = request.user
    level_area.is_deleted=True
    level_area.deleted_at = timezone.now()
    name = level_area.area
    level_area.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "ACCREDITATION LEVEL AREA MODULE"
    activity_log_entry.action = "Archived a record"
    activity_log_entry.type = "ARCHIVE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'{name} is successfully archived!') 
    return redirect('accreditations:program-accreditation-area', pk=ins_pk)




def assign_user(request):
    if request.method == "POST":
        chairman_form = ChairManAssignedToArea_Form(request.POST)
        cochairman_form = CoChairUserAssignedToArea_Form(request.POST)
        member_form = MemberAssignedToArea_Form(request.POST)

        if chairman_form.is_valid() and cochairman_form.is_valid() and member_form.is_valid():
            try:
                with transaction.atomic():
                    chairman_val = request.POST.get('is_chairman')
                    cochairman_val = request.POST.get('is_cochairman')

                    area = instrument_level_area.objects.get(id=int(request.POST.get('area')))

                    if chairman_val is None:
                        return JsonResponse({'error': 'Please select a Chairman for this Area.'}, status=400)
                    else:
                        chairman = CustomUser.objects.get(id=chairman_val)
                        # Check if a chairman is already assigned to the same area
                        if user_assigned_to_area.objects.filter(area=area, is_chairman=True).exists():
                            user_assigned_to_area.objects.filter(area=area, is_chairman=True).delete()
                            chairman_instance = chairman_form.save(commit=False)
                            chairman_instance.assigned_user = chairman
                            chairman_instance.area = area
                            chairman_instance.is_chairman = True
                            chairman_instance.assigned_by = request.user
                            chairman_instance.save()

                        # Check for assignment conflicts in chairman role
                        elif user_assigned_to_area.objects.filter(assigned_user=chairman, area=area).exists():
                            return JsonResponse({'error': f'Area assignment conflict: A Chairman named {chairman.first_name} {chairman.last_name} cannot be assigned to the same area more than once.'}, status=400)

                        else:
                            chairman_instance = chairman_form.save(commit=False)
                            chairman_instance.assigned_user = chairman
                            chairman_instance.area = area
                            chairman_instance.is_chairman = True
                            chairman_instance.assigned_by = request.user
                            chairman_instance.save()
                    
                    if cochairman_val is not None and cochairman_val != 'None':
                        cochairman = CustomUser.objects.get(id=cochairman_val)
                        # Check for assignment conflicts in chairman role
                        if user_assigned_to_area.objects.filter(assigned_user__in=[cochairman], area=area).exists():
                           return JsonResponse({'error': f'Area assignment conflict: A Co-chairman named {cochairman.first_name} {cochairman.last_name} cannot be assigned to the same area more than once.'}, status=400)
                        
                        else: 
                            cochairman_instance = cochairman_form.save(commit=False)
                            cochairman_instance.assigned_user = cochairman
                            cochairman_instance.area = area
                            cochairman_instance.is_cochairman = True
                            cochairman_instance.assigned_by = request.user
                            cochairman_instance.save()
            
                    member_list = request.POST.getlist('is_member')
                    if member_list:
                        print('Member List: ', member_list)
                        count = 1
                        for member_id in member_list:
                            if count <= 5:
                                member = CustomUser.objects.get(id=int(member_id))
                                
                                # Check for assignment conflicts
                                if user_assigned_to_area.objects.filter(assigned_user=member, area=area).exists():
                                    return JsonResponse({'error': f'Area assignment conflict: {member.first_name} {member.last_name} user cannot have multiple roles within the same area.'}, status=400)
                                    break

                                member_instance = member_form.save(commit=False)
                                member_instance.assigned_user = member
                                member_instance.area = area
                                member_instance.is_member = True
                                member_instance.assigned_by = request.user
                                member_instance.save()
                                print('Counts: ', count)
                            else:
                                return JsonResponse({'error': 'The System can only accepts Five (5) members per areas.'}, status=400)
                                break
                            count += 1
       

                messages.success(request, "Area Managers are successfully assigned!")
                return JsonResponse({'status': 'success'}, status=200)

            except IntegrityError as e:
                return JsonResponse({'error': 'Oops! It seems like you selected a user who is already assigned to this area. Please choose a different user.'}, status=400)
        else:
            # Form validation failed
            errors = {
                'chairman_form_errors': chairman_form.errors,
                'cochairman_form_errors': cochairman_form.errors,
                'member_form_errors': member_form.errors
            }
            return JsonResponse(errors, status=400)

#------------------------------------------------------------[ ARCHIVE PAGE CODES ]------------------------------------------------------------#
@login_required
@permission_required("Accreditation.delete_instrument_level_area", raise_exception=True)
def archive_landing(request, pk):
    records = instrument_level_area.objects.select_related('instrument_level').select_related('area').filter(instrument_level=pk, is_deleted= True) #Getting all the data inside the Program table and storing it to the context variable

    details = []
     # Iterate through each record and create an update form for it
    for record in records:
        update_form =  Create_LevelArea_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form,created_by, modified_by))

    context = { 'details': details, 'pk': pk , 'records': records}#Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-page/instrument-area/archive-page/landing-page.html', context)

@login_required
@permission_required("Accreditation.delete_instrument_level_area", raise_exception=True)
def restore(request, ins_pk, pk):
    # Gets the records who have this ID
    level_area = instrument_level_area.objects.get(id=pk)

    #After getting that record, this code will restore it.
    level_area.modified_by = request.user
    level_area.deleted_at = None
    level_area.is_deleted=False
    name = level_area.area
    level_area.save()

    # Create an instance of the ActivityLog model
    activity_log_entry = activity_log()

    # Set the attributes of the instance
    activity_log_entry.module = "ACCREDITATION LEVEL AREA MODULE"
    activity_log_entry.action = "Restored a record"
    activity_log_entry.type = "RESTORE"
    activity_log_entry.datetime_acted =  timezone.now()
    activity_log_entry.acted_by = request.user
    # Set other attributes as needed

    # Save the instance to the database
    activity_log_entry.save()

    messages.success(request, f'{name} is successfully restored!') 
    return redirect('accreditations:program-accreditation-area-archive-page', pk=ins_pk)
