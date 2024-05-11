import math
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Accreditation.forms import ReviewUploadBin_Form
# from Accreditation.models import component_upload_bin, uploaded_evidences
from Accreditation.models import files, instrument_level_folder, program_accreditation
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
import datetime
# Create your views here.
@login_required
def landing_page(request):
	review_form = ReviewUploadBin_Form(request.POST or None)
	
	records = instrument_level_folder.objects.select_related('instrument_level', 'parent_directory').filter(is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable
	#Getting all the data inside the Program table and storing it to the context variable
	under_accred_records = program_accreditation.objects.select_related('instrument_level', 'program').filter(is_deleted= False, is_done=False) 
	under_accred_programs_count = program_accreditation.objects.filter(is_deleted= False, is_done=False).count() 	#This code counts the programs taht under accreditation
	# reviewable_folders = instrument_level_folder.objects.select_related('parent_directory', 'instrument_level').filter(is_deleted = False, can_be_reviewed=True)
	reviewable_folders = instrument_level_folder.objects.filter(~Q(progress_percentage=100.00), ~Q(rating=5.00), Q(has_progress_bar=True) | Q(can_be_reviewed = True), is_deleted= False).order_by('name') #Getting all the data inside the Program table and storing it to the context variable
	uploaded_files = files.objects.select_related('instrument_level', 'parent_directory').filter(is_deleted = False)

	accredited_records = program_accreditation.objects.select_related('instrument_level', 'program').filter(is_deleted= False, is_done=True, is_failed = False) 
	accredited_program_count = program_accreditation.objects.filter(is_deleted= False, is_done=True).count() 

	progress_percentage_result = progress_precentage_cacl(under_accred_records)
	accreditation_summary = program_accreditation_summary(under_accred_records, accredited_records)

	survey_ready_data = survey_visit_ready()
	awaiting_result_data = awaiting_result()
	recieved_certification_data = recieved_certification()
	survey_revisit_data = survey_revisit()
	failed_result_data = failed_result()
	progress_percentage_count = programs_progress_percentage_count(under_accred_records)


	context = { 'under_accred_records': under_accred_records,
				'under_accred_programs_count': under_accred_programs_count,
				'progress_percentage_result':progress_percentage_result,
				'accreditation_summary': accreditation_summary,
				'accredited_records': accredited_records,
				'accredited_program_count': accredited_program_count,
				'survey_ready_data': survey_ready_data,
				'awaiting_result_data': awaiting_result_data,
				'progress_percentage_count': progress_percentage_count,
				'recieved_certification_data': recieved_certification_data,
				'survey_revisit_data': survey_revisit_data,
				'failed_result_data': failed_result_data,
				'reviewable_folders': reviewable_folders,
				'uploaded_files': uploaded_files,
				'records': records,
				# 'uploaded_records':	uploaded_records,
				'review_form': review_form 
			}  #Getting all the data inside the type table and storing it to the context variable

	#Getting all the data inside the Program table and storing it to the context variable
	return render(request, 'dashboard_landing/dashboard_landing.html', context)


def progress_precentage_cacl(under_accred_records):
	# Calculating the overall progress percentage of the all under accreditation program
	progress=0.00
	progress_percentage_result=0.00
	overall_progress=0.00
	count = 0
	for record in under_accred_records:
		if record.instrument_level.progress_percentage:
			progress += float(record.instrument_level.progress_percentage)
		count+=1
	
	overall_progress = 100 * count
	if progress and overall_progress:
		progress_percentage_result= (progress / overall_progress) * 100
		progress_percentage_result = round(progress_percentage_result, 2)
	return progress_percentage_result


def program_accreditation_summary(under_accred_records, accredited_records):


	under_accred_summary = {'level_1': 0, 'level_2': 0, 'level_3': 0, 'level_4': 0}
	accredited_summary = {'level_1': 0, 'level_2': 0, 'level_3': 0, 'level_4': 0}

	for record in under_accred_records:
		if record.instrument_level.level.name == 'LEVEL I':
			under_accred_summary['level_1'] += 1

		elif record.instrument_level.level.name == 'LEVEL II':
			under_accred_summary['level_2']  += 1

		elif record.instrument_level.level.name == 'LEVEL III':
			under_accred_summary['level_3']  += 1

		elif record.instrument_level.level.name == 'LEVEL IV':
			under_accred_summary['level_4']  += 1


	for record in accredited_records:
		if record.instrument_level.level.name == 'LEVEL I':
			accredited_summary['level_1'] += 1

		elif record.instrument_level.level.name == 'LEVEL II':
			accredited_summary['level_2']  += 1

		elif record.instrument_level.level.name == 'LEVEL III':
			accredited_summary['level_3']  += 1

		elif record.instrument_level.level.name == 'LEVEL IV':
			accredited_summary['level_4']  += 1

	accreditation_summary = {'accredited_summary': accredited_summary, 'under_accred_summary':under_accred_summary}

	return accreditation_summary


def survey_visit_ready():
	survey_ready_records = program_accreditation.objects.select_related('instrument_level', 'program').filter(is_deleted=False, is_done=False, instrument_level__progress_percentage =100.0)
	count = 0
	for record in survey_ready_records:
		count += 1
	survey_ready_data = {'survey_ready_records': survey_ready_records, 'survey_ready_count': count}
	return survey_ready_data


# This functions get the records with survey_visit_date greater than or equal to one week from now
def awaiting_result():
	current_datetime = timezone.now()
	one_day_after = current_datetime + timezone.timedelta(days=1)
	current_date = current_datetime.date()

	# Filter records based on conditions
	under_accred_records = program_accreditation.objects.select_related('instrument_level', 'program').filter(
		(
			Q(revisit_date__isnull=True, survey_visit_date__lte=one_day_after) | 
			Q(revisit_date__lte=one_day_after)
		) & 
		 ~Q(revisit_date__date=current_date),  # Exclude records where revisit_date is the same as current_datetime
		is_deleted=False, is_done=False, is_failed=False
	)
	count = 0
	for record in under_accred_records:
		count += 1

	awaiting_result_data = {'awaiting_result_records': under_accred_records, 'awaiting_result_count': count}
	return awaiting_result_data
	

def recieved_certification():
	recieved_certification_records = program_accreditation.objects.select_related('instrument_level', 'program').filter(is_deleted=False, is_done=True, status="PASSED")
	count = 0
	for record in recieved_certification_records:
		count += 1
	recieved_certification_data = {'recieved_certification_records': recieved_certification_records, 'recieved_certification_count': count}
	return recieved_certification_data

def survey_revisit():
	# Get the current date and time
	current_datetime = timezone.now()

	# Filter records based on conditions
	survey_revisit_records = program_accreditation.objects.select_related('instrument_level', 'program').filter(
		is_deleted=False,
		is_done=False,
		status="SUBJECT FOR SURVEY REVISIT",
		revisit_date__gte=datetime.date.today()  # Updated line
	)


	# survey_revisit_records = program_accreditation.objects.select_related('instrument_level', 'program').filter(is_deleted=False, is_done=False, status="SUBJECT FOR SURVEY REVISIT")
	count = 0
	for record in survey_revisit_records:
		count += 1
	survey_revisit_data = {'survey_revisit_records': survey_revisit_records, 'survey_revisit_count': count}
	return survey_revisit_data

def failed_result():
	failed_result_records = program_accreditation.objects.select_related('instrument_level', 'program').filter(is_deleted=False, is_done=True, is_failed=True, status="FAILED")
	count = 0
	for record in failed_result_records:
		count += 1
	failed_result_data = {'failed_result_records': failed_result_records, 'failed_result_count': count}
	return failed_result_data




def programs_progress_percentage_count(under_accred_records):

	count_0 = 0
	count_11 = 0
	count_21 = 0	
	count_31 = 0
	count_41 = 0
	count_51 = 0
	count_61 = 0
	count_71 = 0	
	count_81 = 0
	count_91 = 0

	for record in under_accred_records:
		if record.instrument_level.progress_percentage:
			percentage = record.instrument_level.progress_percentage
		else:
			percentage = 0

		if percentage >= 0 and percentage <= 10:
			count_0 += 1

		elif percentage >= 11 and percentage <= 20:
			count_11 += 1

		elif percentage >= 21 and percentage <= 30:
			count_21 += 1

		elif percentage >= 31 and percentage <= 40:
			count_31 += 1

		elif percentage >= 41 and percentage <= 50:
			count_41 += 1

		elif percentage >= 51 and percentage <= 60:
			count_51 += 1
			
		elif percentage >= 61 and percentage <= 70:
			count_61 += 1

		elif percentage >= 71.0 and percentage <= 80.0:
			count_71 += 1

		elif percentage >= 81.0 and percentage <= 90.0:
			count_81 += 1

		elif percentage >= 91.0 and percentage <= 100.0:
			count_91 += 1

	data = {
				'count_0': count_0,
				'count_11': count_11,
				'count_21': count_21,
				'count_31': count_31,
				'count_41': count_41,
				'count_51': count_51,
				'count_61': count_61,
				'count_71': count_71,
				'count_81': count_81,
				'count_91': count_91,
	}

	return data


@login_required
def folder_view(request, pk, record_id):
   
    #Getting the data from the API
    uploaded_files = files.objects.filter(parent_directory=pk, is_deleted=False)
    records = instrument_level_folder.objects.select_related('instrument_level', 'parent_directory').filter(is_deleted= False, parent_directory=pk) #Getting all the data inside the table and storing it to the context variable
    parent_folder = instrument_level_folder.objects.select_related('parent_directory').get(is_deleted=False, id=pk) #Getting the data of the parent folder


    #Getting all the data inside the type table and storing it to the context variable
    context = { 'records': records, 
                'pk': pk,
                'parent_folder': parent_folder,
                'uploaded_files': uploaded_files,
				'is_child': True,
				'record_id': record_id
               }  

    return render(request, 'dashboard_landing/folder-cards.html', context)

