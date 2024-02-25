from django.http import JsonResponse
from django.shortcuts import render
import requests
from datetime import datetime, timedelta
from django.utils import timezone

from django.contrib.auth.decorators import login_required

from Accreditation.models import program_accreditation

@login_required
def faculty_awards_info(request, program_accred_pk):
    # API endpoint URL
    api_url = 'https://pupqcfis-com.onrender.com/api/FISFaculty/Professional-Development'

    api_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiI1NGY0NzRmMTAxYTc0NWRhYmRiODU1M2I4YzYzMzliMSJ9.hNjCSVI3bsaivK3JlAOqGBlrMkvZxUptUxSqCCD5STs'

    #HEADER CONFIGURATION
    headers = {  
        'Authorization': 'API-Key',
        'token': api_token,
        } 
    
    try:
        # Make GET request to API with headers
        response = requests.get(api_url, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            current_data = response.json()
            faculty_details = faculty_list()

            # Get the record that has an id equal to program_accred_pk
            accred_program = program_accreditation.objects.select_related('instrument_level', 'program').get(id=program_accred_pk)

            #Get the date of the actual survey
            survey_date = accred_program.survey_visit_date
            # Parse the string to a datetime object
            survey_date_obj = datetime.strptime(str(survey_date), "%Y-%m-%d %H:%M:%S%z")
            # Format the datetime object as a string in the desired format
            formatted_survey_date = survey_date_obj.strftime("%Y-%m-%d %H:%M:%S")



            # Calculate the start date three years prior to the survey date
            start_date_range = survey_date - timedelta(days=3*365)
            # Parse the string to a datetime object
            date_range_obj = datetime.strptime(str(start_date_range), "%Y-%m-%d %H:%M:%S%z")
            # Format the datetime object as a string in the desired format
            formatted_date_range = date_range_obj.strftime("%Y-%m-%d %H:%M:%S")


            new_data = []

            for data_entry in current_data:
                faculty_id = str(data_entry["FacultyId"])  # Convert faculty_id to string for comparison
                # Parse the string to a datetime object
                date_start = datetime.strptime(data_entry["date_start"], "%a, %d %b %Y %H:%M:%S %Z")
                # Format the datetime object as a string in the desired format
                formatted_date_str = date_start.strftime("%Y-%m-%d %H:%M:%S%z")

                # Assuming data_entry["date_start"] and data_entry["date_end"] are strings representing dates
                date_start = timezone.make_aware(datetime.strptime(data_entry["date_start"], "%a, %d %b %Y %H:%M:%S %Z"))
                date_end = timezone.make_aware(datetime.strptime(data_entry["date_end"], "%a, %d %b %Y %H:%M:%S %Z"))

                # Format the dates as required
                formatted_date_start = date_start.strftime("%b %d, %Y %I:%M%p")
                formatted_date_end = date_end.strftime("%b %d, %Y %I:%M%p")


                if faculty_id in faculty_details["Faculties"]:
                    if formatted_date_range <=  formatted_date_str <=  formatted_survey_date :
                        details_entry = faculty_details["Faculties"][faculty_id]
                        new_entry = {
                            "id": data_entry["id"],
                            "FacultyId": data_entry["FacultyId"],
                            "FirstName": details_entry["FirstName"],
                            "LastName": details_entry["LastName"],
                            "MiddleNamee": details_entry["MiddleName"],
                            "MiddleInitial": details_entry["MiddleInitial"],
                            "title": data_entry["title"],
                            "date_start": formatted_date_start,
                            "date_end": formatted_date_end,
                            "hours": data_entry["hours"],
                            "conducted_by": data_entry["conducted_by"],
                            "type": data_entry["type"],
                            "file_id": data_entry["file_id"]
                        }
                        new_data.append(new_entry)

            # Pass data to template context
            # return render(request, 'my_template.html', {'api_data': data})
            # return JsonResponse({'records': new_data})
            return render(request,'faculty-info-system/faculty-awards/landing-page.html' ,{'records': new_data, 'program_accred_pk': program_accred_pk})
        else:
            # Handle unsuccessful request
            return JsonResponse({'error': f"Failed to fetch data from the API: {response.status_code}"}, status=500)
    except requests.RequestException as e:
        # Handle request exception
        return JsonResponse({'error': f"Request to API failed: {e}"}, status=500)
    


def faculty_list():
    # API endpoint URL
    api_url = 'https://pupqcfis-com.onrender.com/api/all/FISFaculty'

    api_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiI1NGY0NzRmMTAxYTc0NWRhYmRiODU1M2I4YzYzMzliMSJ9.hNjCSVI3bsaivK3JlAOqGBlrMkvZxUptUxSqCCD5STs'

    #HEADER CONFIGURATION
    headers = {  
        'Authorization': 'API-Key',
        'token': api_token,
        } 
    
    try:
        # Make GET request to API with headers
        response = requests.get(api_url, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            return data
        else:
            # Handle unsuccessful request
            return JsonResponse({'error': f"Failed to fetch data from the API: {response.status_code}"}, status=500)
    except requests.RequestException as e:
        # Handle request exception
        return JsonResponse({'error': f"Request to API failed: {e}"}, status=500)
    


