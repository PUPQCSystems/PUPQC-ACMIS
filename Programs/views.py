from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
details = [{'program_name': 'Bachelor of Science in Information Technology',
                'Abbreviation': 'BSIT',
                'modified_by': 'Jonel Malinao',
                'modified_at': 'January 12, 2023'},
                {'program_name': 'Bachelor of Science in Computer Science',
                'Abbreviation': 'BSCS',
                'modified_by': 'Jonel Malinao',
                'modified_at': 'January 12, 2023'},
                {'program_name': 'Bachelor of Science in Computer Engineering',
                'Abbreviation': 'BSCE',
                'modified_by': 'Jonel Malinao',
                'modified_at': 'January 12, 2023'}
                ]



def landing_page(request):
    context = { 'records': details } 
    return render(request, 'landing_page/landing_page.html', context)
