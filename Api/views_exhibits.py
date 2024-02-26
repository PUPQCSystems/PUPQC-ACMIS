import requests
from rest_framework import generics, serializers
from Accreditation.models import program_accreditation
from Users.models import category_training, faculty_certificates, seminar_workshop_training
from .serializers import CategorySerializer, FacultyCertificateSerializer, ProgramAccreditationSerializer, WorkshopsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import QueryDict


@login_required
def landing_page(request, program_accred_pk):
    
        # API endpoint URL
    api_url = 'https://research-info-system-qegn.onrender.com/integration/faculty/research-papers/list'

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

            print(data)
            # Codes for converting keys with spaces to no spaces
            for item in data:
                new_data = {}
                # Iterate over the key-value pairs in the current dictionary
                for key, value in item.items():
                    # Remove spaces from the key and assign the value to the new key
                    new_key = key.replace(' ', '')
                    new_data[new_key] = value
                # Replace the old dictionary with the new one in the list
                data[data.index(item)] = new_data


            # Pass data to template context
            # return render(request, 'my_template.html', {'api_data': data})
            # return JsonResponse({'api_data': data})
            return render(request,'exhibit-page/landing-page.html' ,{'records': data, 'program_accred_pk':program_accred_pk})
        else:
            # Handle unsuccessful request
            return JsonResponse({'error': f"Failed to fetch data from the API: {response.status_code}"}, status=500)
    except requests.RequestException as e:
        # Handle request exception
        return JsonResponse({'error': f"Request to API failed: {e}"}, status=500)


