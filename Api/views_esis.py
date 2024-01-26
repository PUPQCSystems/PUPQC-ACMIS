from django.shortcuts import render
import requests

from django.contrib.auth.decorators import login_required

@login_required
def extension_info(request):
    try:
        records = requests.get('https://univ-esis.onrender.com/api/extension-programs/finished-projects?fbclid=IwAR1DbWqmhoSPC039g4z1TJB9KC2VYdiVTndVeN_HPItch4CBl-5ayzHrnFY').json()
    except requests.RequestException as e:
        # Handle the error, log it, or provide a default value
        records = []
    
    print('HAHAHA', records)


    return render(request, 'extension-services-info-system/landing-page.html', { 'records':records})

