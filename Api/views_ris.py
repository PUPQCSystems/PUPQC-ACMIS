from django.http import JsonResponse
from django.shortcuts import render
import requests
from rest_framework import generics, serializers
from Accreditation.models import accreditation_records, program_accreditation
from .serializers import AccreditationRecordSerializer
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def research_info(request):
    # Replace YOUR_BEARER_TOKEN with the actual bearer token
    bearer_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGVzdF91c2VyIiwidG9rZW5fZ2VuZXJhdGUiOiJzdWNjZXNzIiwiY29ubmVjdGlvbl90eXBlIjoiZm9yIGludGVncmF0aW9uIn0.TYFxVaUUK-hbOMpWzcYhnXA4ZKQgeitWSrTyKpIuU-g'
    api_url = 'https://research-info-system-qegn.onrender.com/integration/accre/list/papers'

    headers = {
        'Authorization': bearer_token,
                          
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            # Parse the response JSON if needed
            api_data = response.json()

            # Pass the API data to the template
            return render(request, 'research-info-system/landing-page.html', {'api_data':api_data})
        else:
            # Handle other response codes
            return JsonResponse({'error': 'Failed to fetch data from the API'}, status=response.status_code)

    except requests.RequestException as e:
        # Handle request exceptions
        return JsonResponse({'error': str(e)}, status=500)
    
