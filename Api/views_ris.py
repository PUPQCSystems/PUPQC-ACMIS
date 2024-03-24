from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
import os, requests, json
from datetime import date, timedelta, datetime
from django.utils import timezone

# from Accreditation.models import program_accreditation

@login_required
def research_faculty(request, program_accred_pk):
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

            # # Get the record that has an id equal to program_accred_pk
            # accred_program = program_accreditation.objects.select_related('instrument_level', 'program').get(id=program_accred_pk)

            # #Get the date of the actual survey
            # survey_date = accred_program.survey_visit_date

            # Calculate the start date three years prior to the survey date
            # date_range = survey_date - timedelta(days=3*365)

            new_data = []

            # Assuming data is defined properly
            # for research in data:
            #     publish_date = timezone.make_aware(datetime.strptime(research['research_paper']['date_publish'],"%Y-%m-%d"))

            #     if date_range <= publish_date <= survey_date:
            #         new_entry = {
            #             'research_paper': {
            #                 "title": research['research_paper']['title'],
            #                 "content": research['research_paper']['content'],
            #                 "abstract": research['research_paper']['abstract'],
            #                 "file": research['research_paper']['file'],
            #                 "date_publish": publish_date,
            #                 "authors": research['research_paper']['authors']
            #             }
            #         }
            #         new_data.append(new_entry)
            
            # Pass data to template context
            # return render(request, 'my_template.html', {'api_data': data})
            # return JsonResponse({'api_data': data})
            context =   {   'records': new_data,
                            'program_accred_pk': program_accred_pk, 
                            # 'accred_program': accred_program,
                            # 'date_range': date_range
                        }
            return render(request,'research-info-system/faculty-research/landing-page.html', context)
        else:
            # Handle unsuccessful request
            return JsonResponse({'error': f"Failed to fetch data from the API: {response.status_code}"}, status=500)
    except requests.RequestException as e:
        # Handle request exception
        return JsonResponse({'error': f"Request to API failed: {e}"}, status=500)
    
@login_required
def research_student(request, program_accred_pk):
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

            # Get the record that has an id equal to program_accred_pk
            accred_program = program_accreditation.objects.select_related('instrument_level', 'program').get(id=program_accred_pk)

            #Get the date of the actual survey
            survey_date = accred_program.survey_visit_date

            # Calculate the start date three years prior to the survey date
            date_range = survey_date - timedelta(days=3*365)

            new_data = []

            # Assuming data is defined properly
            for research in data:
                publish_date = timezone.make_aware(datetime.strptime(research['research_paper']['date_publish'],"%Y-%m-%d"))

                if date_range <= publish_date <= survey_date:
                    new_entry = {
                        'research_paper': {
                            "title": research['research_paper']['title'],
                            "content": research['research_paper']['content'],
                            "abstract": research['research_paper']['abstract'],
                            "file": research['research_paper']['file'],
                            "date_publish": publish_date,
                            "authors": research['research_paper']['authors']
                        }
                    }
                    new_data.append(new_entry)
            
            # Pass data to template context
            # return render(request, 'my_template.html', {'api_data': data})
            # return JsonResponse({'api_data': data})
            context =   {   'records': new_data,
                            'program_accred_pk': program_accred_pk, 
                            'accred_program': accred_program,
                            'date_range': date_range
                        }
            return render(request,'research-info-system/student-research/landing-page.html', context)
        else:
            # Handle unsuccessful request
            return JsonResponse({'error': f"Failed to fetch data from the API: {response.status_code}"}, status=500)
    except requests.RequestException as e:
        # Handle request exception
        return JsonResponse({'error': f"Request to API failed: {e}"}, status=500)