from django.utils import timezone
from django.views import View
from rest_framework import generics, viewsets, status
from django.shortcuts import render, redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import instrument, instrument_level #Import the model for data retieving
from Accreditation.serializers import InstrumentSerializer
from .forms import Create_Instrument_Form, Create_InstrumentLevel_Form
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

class InstrumentLevelList(View):
    def get(self, request, pk):
        #Getting the data from the API
        create_form = Create_InstrumentLevel_Form(request.POST or None)
        records = instrument_level.objects.select_related('instrument').filter(instrument=pk,is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable

        # Initialize an empty list to store update forms for each record
        details = []

        # Iterate through each record and create an update form for it
        for record in records:
            update_form = Create_InstrumentLevel_Form(instance=record)
            created_by = record.created_by  # Get the user who created the record
            modified_by = record.modified_by  # Get the user who modified the record
            details.append((record, update_form, created_by, modified_by))

        context = { 'records': records, 'create_form': create_form, 'details': details, 'pk': pk}  #Getting all the data inside the type table and storing it to the context variable

        return render(request, 'accreditation-instrument-level/main-page/landing-page.html', context)
    
    def post(self, request, pk):
        create_form = Create_InstrumentLevel_Form(request.POST or None)

        if create_form.is_valid():
            create_form.instance.created_by = request.user
            create_form.instance.instrument_id = pk
            create_form.save()
            name = create_form.cleaned_data.get('name')
            messages.success(request, f"{name} accreditation instrument's level is successfully created!") 
            # url_landing = "{% url 'accreditations:type' %}"
            return JsonResponse({'status': 'success'}, status=200)
        else:
            # Return a validation error using a JSON response
            return JsonResponse({'errors': create_form.errors}, status=400)
        