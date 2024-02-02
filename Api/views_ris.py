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
            return render(request,'research-info-system/faculty-research/landing-page.html' ,{'records': data})
        else:
            # Handle unsuccessful request
            return JsonResponse({'error': f"Failed to fetch data from the API: {response.status_code}"}, status=500)
    except requests.RequestException as e:
        # Handle request exception
        return JsonResponse({'error': f"Request to API failed: {e}"}, status=500)
    

def research_student(request, format=None):
    # API endpoint URL
    api_url = 'https://research-info-system-qegn.onrender.com/integration/accre/list/papers'

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

            # Initialize a list to store modified dictionaries
            new_data_list = []

            # Loop through each item in the data list
            for item in data:
                # Remove spaces from keys and store the modified dictionary
                new_data = {key.replace(' ', ''): value for key, value in item.items()}

                # Separate the 'Course' key and move one course to the main item
                courses = []  # Create a list to store course information
                for researcher in item['Researchers']:
                    course = researcher.pop('Course')  # Extract and remove 'Course' from researcher dictionary
                    if course not in courses:  # Check if the course is not already added
                        courses.append(course)  # Add course information to courses list
                    student_number = researcher.pop('Student Number')  # Extract and remove 'Student Number' from researcher dictionary
                    researcher['StudentNumber'] = student_number  # Add 'StudentNumber' key without spaces
                new_data['Courses'] = courses[:1]  # Add only the first course to the main item

                # Append the modified dictionary to the new_data_list
                new_data_list.append(new_data)

            # Replace the old data list with the modified list
            data = new_data_list

            # Pass data to template context or return JSON response
            # return JsonResponse({'api_data': data})
            return render(request,'research-info-system/student-research/landing-page.html' ,{'records': data})
        else:
            # Handle unsuccessful request
            return JsonResponse({'error': f"Failed to fetch data from the API: {response.status_code}"}, status=500)
    except requests.RequestException as e:
        # Handle request exception
        return JsonResponse({'error': f"Request to API failed: {e}"}, status=500)