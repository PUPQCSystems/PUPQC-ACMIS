# @login_required
# def research_info(request):
#     # Replace YOUR_BEARER_TOKEN with the actual bearer token
#     bearer_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGVzdF91c2VyIiwidG9rZW5fZ2VuZXJhdGUiOiJzdWNjZXNzIiwiY29ubmVjdGlvbl90eXBlIjoiZm9yIGludGVncmF0aW9uIn0.TYFxVaUUK-hbOMpWzcYhnXA4ZKQgeitWSrTyKpIuU-g'
#     api_url = 'https://research-info-system-qegn.onrender.com/integration/accre/list/papers'

#     headers = {
#         'Authorization': bearer_token,
                          
#         'Content-Type': 'application/json',
#     }

#     try:
#         response = requests.get(api_url, headers=headers)

#         if response.status_code == 200:
#             # Parse the response JSON if needed
#             api_data = response.json()

#             # Pass the API data to the template
#             return render(request, 'research-info-system/landing-page.html', {'api_data':api_data})
#         else:
#             # Handle other response codes
#             return JsonResponse({'error': 'Failed to fetch data from the API'}, status=response.status_code)

#     except requests.RequestException as e:
#         # Handle request exceptions
#         return JsonResponse({'error': str(e)}, status=500)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
import os, requests, json
from datetime import date

def research_faculty(request, format=None):
    
    # API endpoint URL
    api_url = 'https://research-info-system-qegn.onrender.com/integration/accre/all-papers/faculty'

    # Bearer token
    bearer_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGVzdF91c2VyIiwidG9rZW5fZ2VuZXJhdGUiOiJzdWNjZXNzIiwiY29ubmVjdGlvbl90eXBlIjoiZm9yIGludGVncmF0aW9uIn0.TYFxVaUUK-hbOMpWzcYhnXA4ZKQgeitWSrTyKpIuU-g'

    # Authorization header with bearer token
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    try:
        # Make GET request to API with headers
        response = requests.get(api_url, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            # Pass data to template context
            # return render(request, 'my_template.html', {'api_data': data})
            return JsonResponse({'api_data': data})
            # return render(request,'research-info-system/faculty-research/landing-page.html' ,{'records': data})
        else:
            # Handle unsuccessful request
            return JsonResponse({'error': f"Failed to fetch data from the API: {response.status_code}"}, status=500)
    except requests.RequestException as e:
        # Handle request exception
        return JsonResponse({'error': f"Request to API failed: {e}"}, status=500)
    

def research_student(request, format=None):
    # API endpoint URL
    api_url = 'https://research-info-system-qegn.onrender.com/integration/accre/all-papers/students'

    # Bearer token
    bearer_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGVzdF91c2VyIiwidG9rZW5fZ2VuZXJhdGUiOiJzdWNjZXNzIiwiY29ubmVjdGlvbl90eXBlIjoiZm9yIGludGVncmF0aW9uIn0.TYFxVaUUK-hbOMpWzcYhnXA4ZKQgeitWSrTyKpIuU-g'

    # Authorization header with bearer token
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    try:
        # Make GET request to API with headers
        response = requests.get(api_url, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            # Pass data to template context or return JSON response
            return JsonResponse({'api_data': data})
            # return render(request,'research-info-system/student-research/landing-page.html' ,{'records': data})
        else:
            # Handle unsuccessful request
            return JsonResponse({'error': f"Failed to fetch data from the API: {response.status_code}"}, status=500)
    except requests.RequestException as e:
        # Handle request exception
        return JsonResponse({'error': f"Request to API failed: {e}"}, status=500)