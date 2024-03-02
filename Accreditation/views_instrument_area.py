from django.db import IntegrityError
from django.utils import timezone
from django.views import View
from rest_framework import generics, viewsets, status
from django.shortcuts import render, redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import Group, Permission
from Accreditation.models_views import UserGroupView
from Users.models import CustomUser, activity_log
from .models import accreditation_certificates, component_upload_bin, instrument, instrument_level, instrument_level_area, level_area_parameter, parameter_components, program_accreditation, user_assigned_to_area #Import the model for data retieving
from Accreditation.serializers import InstrumentSerializer
from .forms import ChairManAssignedToArea_Form, CoChairUserAssignedToArea_Form, Create_Instrument_Form, Create_InstrumentLevel_Form, Create_LevelArea_Form, FailedResult_Form, LevelAreaFormSet, MemberAssignedToArea_Form, PassedResult_Form, RevisitResult_Form
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
    passed_result_form = PassedResult_Form(request.POST or None)
    revisit_result_form = RevisitResult_Form(request.POST or None)
    failed_result_form = FailedResult_Form(request.POST or None)
    formset  = LevelAreaFormSet(queryset=instrument_level_area.objects.none())
    # records = instrument_level_area.objects.select_related('instrument_level','area').filter(instrument_level=pk, is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable
    certificates_records = accreditation_certificates.objects.select_related('accredited_program').filter(is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable
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

    print(accred_program.revisit_date)

    context = { 'records': records,
                'details': details, 
                'pk': pk,   
                'area_formset': formset, 
                'user_records': user_records,
                'accred_program': accred_program,
                'chairman_form': chairman_form,
                'cochairman_form': cochairman_form,
                'member_form': member_form,
                'passed_result_form': passed_result_form,
                'failed_result_form': failed_result_form,
                'revisit_result_form': revisit_result_form,
                'certificates_records': certificates_records
                }  #Getting all the data inside the type table and storing it to the context variable

    return render(request, 'accreditation-page/instrument-area/main-page/landing-page.html', context)

@login_required
@permission_required("Accreditation.delete_instrument_level_area", raise_exception=True)
def archive(request, ins_pk, pk, accred_pk):
    # Gets the records who have this ID
    level_area = instrument_level_area.objects.get(id=pk)

    #After getting that record, this code will delete it.
    level_area.modified_by = request.user
    level_area.is_deleted=True
    level_area.deleted_at = timezone.now()
    name = level_area.area
    level_area.save()


#----------------[ Codes for calculating program percentage of the program accreditation/ instument_level ]----------------
    instrument_id = level_area.instrument_level.id
    instrument_record = instrument_level.objects.get(id = instrument_id)

    # Get all child areas of the program accreditation/ instrument level
    areas = instrument_level_area.objects.filter(instrument_level=instrument_record, is_deleted=False)
    if areas.exists():

        # Initialize counters
        all_area_bins = 0
        approved_area_bins = 0
        for area_record in areas:
            # Get all child parameters of the area
            area_parameters = level_area_parameter.objects.filter(instrument_level_area_id=area_record.id, is_deleted=False)

            # Iterate through each parameter
            for parameter in area_parameters:
                # Get all child parameter_components of the parameter
                area_parameter_components = parameter_components.objects.filter(area_parameter_id=parameter.id, is_deleted=False)

                # Count all and approved bins for each component
                all_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components, is_deleted=False).count()
                approved_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components, status="approve", is_deleted=False).count()

                # Increment counters
                all_area_bins += all_bins
                approved_area_bins += approved_bins

        # Calculate progress
        progress = 0.00
        if all_area_bins:
            progress = (approved_area_bins / all_area_bins) * 100
            print("Progress: ", progress)
            # Update the progress_percentage field of the area record
            instrument_record.progress_percentage = progress
            instrument_record.save()
        else:
            instrument_record.progress_percentage = 0.00
            instrument_record.save()

    else:
        # Calculate progress
        instrument_record.progress_percentage = 0.00
        instrument_record.save()


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
    return redirect('accreditations:program-accreditation-area', pk=ins_pk, accred_pk=accred_pk)

@login_required
@permission_required(["Accreditation.add_user_assigned_to_area", "Accreditation.change_user_assigned_to_area", "Accreditation.view_user_assigned_to_area", "Accreditation.delete_user_assigned_to_area"], raise_exception=True)
def assign_user(request):
    if request.method == "POST":
        chairman_form = ChairManAssignedToArea_Form(request.POST)
        cochairman_form = CoChairUserAssignedToArea_Form(request.POST)
        try:
            with transaction.atomic():
                chairman_val = request.POST.get('is_chairman')
                print(chairman_val)
                cochairman_val = request.POST.get('is_cochairman')
                member_list = request.POST.getlist('is_member')
                area = instrument_level_area.objects.get(id=int(request.POST.get('area')))
        
                existing_chairman = user_assigned_to_area.objects.filter(area=area, is_chairman=True).first()
                existing_cochairman = user_assigned_to_area.objects.filter(area=area, is_cochairman=True).first()
                existing_members = user_assigned_to_area.objects.filter(area=area, is_member=True)
                existing_assignment = user_assigned_to_area.objects.filter(area=area)

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
                    existing_chairmen = user_assigned_to_area.objects.filter(area=area, is_chairman=True)

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
                    existing_cochairmen = user_assigned_to_area.objects.filter(area=area, is_cochairman=True)
                    
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
                        conflicting_members = user_assigned_to_area.objects.filter(area=area, is_member=True)
                        if conflicting_members.exists():
                            conflicting_members.delete()
                        
                        for member_id in member_ids:
                            member = CustomUser.objects.get(id=member_id)
                            member_form_instance = MemberAssignedToArea_Form(request.POST)
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

#------------------------------------------------------------[ ARCHIVE PAGE CODES ]------------------------------------------------------------#
@login_required
@permission_required("Accreditation.delete_instrument_level_area", raise_exception=True)
def archive_landing(request, pk, accred_pk):
    records = instrument_level_area.objects.select_related('instrument_level').select_related('area').filter(instrument_level=pk, is_deleted= True) #Getting all the data inside the Program table and storing it to the context variable

    details = []
     # Iterate through each record and create an update form for it
    for record in records:
        update_form =  Create_LevelArea_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form,created_by, modified_by))

    #Getting all the data inside the type table and storing it to the context variable
    context = { 'details': details, 
                'pk': pk , 
                'records': records, 
                'accred_pk':accred_pk}
    return render(request, 'accreditation-page/instrument-area/archive-page/landing-page.html', context)

@login_required
@permission_required("Accreditation.delete_instrument_level_area", raise_exception=True)
def restore(request, ins_pk, pk, accred_pk):
    # Gets the records who have this ID
    level_area = instrument_level_area.objects.get(id=pk)

    #After getting that record, this code will restore it.
    level_area.modified_by = request.user
    level_area.deleted_at = None
    level_area.is_deleted=False
    name = level_area.area
    level_area.save()

#----------------[ Codes for calculating program percentage of the program accreditation/ instument_level ]----------------
    instrument_id = level_area.instrument_level.id
    instrument_record = instrument_level.objects.get(id = instrument_id)

    # Get all child areas of the program accreditation/ instrument level
    areas = instrument_level_area.objects.filter(instrument_level=instrument_record, is_deleted=False)

    # Initialize counters
    all_area_bins = 0
    approved_area_bins = 0
    for area_record in areas:
        # Get all child parameters of the area
        area_parameters = level_area_parameter.objects.filter(instrument_level_area_id=area_record.id, is_deleted=False)

        # Iterate through each parameter
        for parameter in area_parameters:
            # Get all child parameter_components of the parameter
            area_parameter_components = parameter_components.objects.filter(area_parameter_id=parameter.id, is_deleted=False)

            # Count all and approved bins for each component
            all_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components, is_deleted=False).count()
            approved_bins = component_upload_bin.objects.filter(parameter_component__in=area_parameter_components, status="approve", is_deleted=False).count()

            # Increment counters
            all_area_bins += all_bins
            approved_area_bins += approved_bins

    # Calculate progress
    progress = 0.00
    if all_area_bins:
        progress = (approved_area_bins / all_area_bins) * 100
        print("Progress: ", progress)
        # Update the progress_percentage field of the area record
        instrument_record.progress_percentage = progress
        instrument_record.save()

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
    return redirect('accreditations:program-accreditation-area-archive-page', pk=ins_pk, accred_pk=accred_pk)
