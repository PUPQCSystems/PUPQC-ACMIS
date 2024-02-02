from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
import os, requests, json
from datetime import date

@login_required
def landing_page(request):
    # Initialize counters for PL and DL
    PL_count = 0
    DL_count = 0


    # API endpoint URL
    api_url = 'https://student-performance-70l3.onrender.com/api/v1/university-admin/student/achievement/?$skip=0&$top=1000'


    # Authorization header with bearer token
    headers = {
        'X-API-Key': '1b20e3f9-8d44-45b7-96da-02e8001d73e8'
    }

    try:
        # Make GET request to API with headers
        response = requests.get(api_url, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

# Codes for SUM OF PL AND DL
            # Iterate over the records
            for record in data["result"]:
                if record["Lister"] == "President Lister":
                    PL_count += 1
                elif record["Lister"] == "Dean Lister":
                    DL_count += 1            


            context = {
                'records': data,
                'PL_count': PL_count,
                'DL_count': DL_count
            }
            # Pass data to template context
            # return render(request, 'my_template.html', {'api_data': data})
            # return JsonResponse( data)
            return render(request, 'student-award-page/landing-page.html', context)
        
        else:
            # Handle unsuccessful request
            return JsonResponse({'error': f"Failed to fetch data from the API: {response.status_code}"}, status=500)
    except requests.RequestException as e:
        # Handle request exception
        return JsonResponse({'error': f"Request to API failed: {e}"}, status=500)
