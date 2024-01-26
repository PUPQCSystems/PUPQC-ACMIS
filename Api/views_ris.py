from django.shortcuts import render
import requests
from rest_framework import generics, serializers
from Accreditation.models import accreditation_records, program_accreditation
from .serializers import AccreditationRecordSerializer
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def research_info(request):
    try:
        records = requests.get('http://127.0.0.1:8000/accreditation/instrument/api/list/').json()
    except requests.RequestException as e:
        # Handle the error, log it, or provide a default value
        records = []
    
    context = { 'records':records }

    return render(request, 'accreditation-parameter-component/main-page/landing-page.html', context)