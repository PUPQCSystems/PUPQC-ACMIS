import math
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Accreditation.models import program_accreditation

# Create your views here.
@login_required
def landing_page(request):
	
	#Getting all the data inside the Program table and storing it to the context variable
	under_accred_records = program_accreditation.objects.select_related('instrument_level', 'program').filter(is_deleted= False, is_done=False) 

	#This code counts the programs taht under accreditation
	under_accred_programs_count = program_accreditation.objects.select_related('instrument_level', 'program').filter(is_deleted= False, is_done=False).count()

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
	if progress:
		progress_percentage_result= (progress / overall_progress) * 100

	context = { 'under_accred_records': under_accred_records,
				'under_accred_programs_count': under_accred_programs_count,
				'progress_percentage_result':progress_percentage_result,
			}  #Getting all the data inside the type table and storing it to the context variable

	#Getting all the data inside the Program table and storing it to the context variable
	return render(request, 'dashboard_landing/dashboard_landing.html', context)
