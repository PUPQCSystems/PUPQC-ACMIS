import math
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Accreditation.models import program_accreditation

# Create your views here.
@login_required
def landing_page(request):
		
	records = program_accreditation.objects.select_related('instrument_level', 'program').filter(is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable
	slide_count = program_accreditation.objects.select_related('instrument_level', 'program').filter(is_deleted= False).count()

	loop_counts = 0
	loop_counts =  math.ceil(slide_count / 3)

	print(loop_counts)

	context = { 'records': records, 'loop_counts': loop_counts}  #Getting all the data inside the type table and storing it to the context variable

	#Getting all the data inside the Program table and storing it to the context variable
	return render(request, 'dashboard_landing/dashboard_landing.html', context)
