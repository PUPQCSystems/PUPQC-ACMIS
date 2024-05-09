from django.shortcuts import render
import requests
import json
from django.contrib.auth.decorators import login_required

@login_required
def extension_info(request, program_accred_pk):
    try:
        records = requests.get('https://univ-esis.onrender.com/api/extension-programs/finished-projects').json()
    except requests.RequestException as e:
        with open('ESIS_data.json') as f:  # Replace with the correct path
            json_data = json.load(f)
        records = json_data


    return render(request, 'extension-services-info-system/landing-page.html', {'records':records, 'program_accred_pk':  program_accred_pk})

