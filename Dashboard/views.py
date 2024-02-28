import math
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Accreditation.forms import ReviewUploadBin_Form
from Accreditation.models import component_upload_bin, program_accreditation, uploaded_evidences
from datetime import datetime, timedelta
from django.db.models import F
from django.db.models import F, ExpressionWrapper, DurationField
from django.utils import timezone
# Create your views here.
@login_required
def landing_page(request):
	review_form = ReviewUploadBin_Form(request.POST or None)
	
	#Getting all the data inside the Program table and storing it to the context variable
	under_accred_records = program_accreditation.objects.select_related('instrument_level', 'program').filter(is_deleted= False, is_done=False) 
	under_accred_programs_count = program_accreditation.objects.filter(is_deleted= False, is_done=False).count() 	#This code counts the programs taht under accreditation
	upload_bins = component_upload_bin.objects.select_related('parameter_component').filter(is_deleted = False, status='ur')
	uploaded_records = uploaded_evidences.objects.select_related('upload_bin', 'uploaded_by').filter(is_deleted = False)

	accredited_records = program_accreditation.objects.select_related('instrument_level', 'program').filter(is_deleted= False, is_done=True) 
	accredited_program_count = program_accreditation.objects.filter(is_deleted= False, is_done=True).count() 

	progress_percentage_result = progress_precentage_cacl(under_accred_records)
	accreditation_summary = program_accreditation_summary(under_accred_records, accredited_records)

	survey_ready_data = survey_visit_ready()
	awaiting_result_data = awaiting_result()
	progress_percentage_count = programs_progress_percentage_count(under_accred_records)
	print(	progress_percentage_count)

	context = { 'under_accred_records': under_accred_records,
				'under_accred_programs_count': under_accred_programs_count,
				'progress_percentage_result':progress_percentage_result,
				'accreditation_summary': accreditation_summary,
				'accredited_records': accredited_records,
				'accredited_program_count': accredited_program_count,
				'survey_ready_data': survey_ready_data,
				'awaiting_result_data': awaiting_result_data,
				'progress_percentage_count': progress_percentage_count,
				'upload_bins': upload_bins,
				'uploaded_records':	uploaded_records,
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
	survey_ready_records = program_accreditation.objects.select_related('instrument_level', 'program').filter(is_deleted=False, is_done=False, instrument_level__progress_percentage__gte=70.0)
	count = 0
	for record in survey_ready_records:
		count += 1
	survey_ready_data = {'survey_ready_records': survey_ready_records, 'survey_ready_count': count}
	return survey_ready_data


# This functions get the records with survey_visit_date greater than or equal to one week from now
def awaiting_result():
# Calculate the date seven days ago
	seven_days_ago = timezone.now() - timedelta(days=7)

	# Filter records where the survey visit date is seven days or more in the past
	under_accred_records = program_accreditation.objects.select_related('instrument_level', 'program').filter(
		is_deleted=False,
		is_done=False,
		survey_visit_date__lte=seven_days_ago
	)

	count = 0
	for record in under_accred_records:
		count += 1

	awaiting_result_data = {'awaiting_result_records': under_accred_records, 'awaiting_result_count': count}
	return awaiting_result_data
	


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
