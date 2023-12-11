from django.views import View
from rest_framework import generics, viewsets, status
from django.shortcuts import render, redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import instrument #Import the model for data retieving
from Accreditation.serializers import InstrumentSerializer
from .forms import Create_Instrument_Form
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field

#This function gets the list of data from the api and then load it to the html file
# This is a function that gets the data from the api and then show the data in html
class InstrumentList(View):
    def get(self, request):
        #Getting the data from the API
        create_form = Create_Instrument_Form(request.POST or None)
        records =instrument.objects.select_related('accredbodies').filter(is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable

        # Initialize an empty list to store update forms for each record
        details = []

        # Iterate through each record and create an update form for it
        for record in records:
            update_form = Create_Instrument_Form(instance=record)
            created_by = record.created_by  # Get the user who created the record
            modified_by = record.modified_by  # Get the user who modified the record
            details.append((record, update_form, created_by, modified_by))
            
        context = { 'records': records, 'create_form': create_form, 'details': details}  #Getting all the data inside the type table and storing it to the context variable

        return render(request, 'accreditation-instrument/landing_page.html', context)
    
    def post(self, request):
        create_form = Create_Instrument_Form(request.POST or None)
        if create_form.is_valid():
            create_form.instance.created_by = request.user
            create_form.save()
            name = create_form.cleaned_data.get('name')
            messages.success(request, f'{name} accreditation type is successfully created!') 
            url_landing = "{% url 'accreditations:type' %}"
            return JsonResponse({'url_landing': url_landing}, status=200)

        else:
            # Return a validation error using a JSON response
            return JsonResponse({'errors': create_form.errors}, status=400)









#------------------------------------------------------------[ CODES JUST FOR EXAMPLE IN API ]------------------------------------------------------------*



#The below code is an API view, its allows the system to get the data and render it in html tamplate
# class InstrumentList(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'accreditation-instrument/landing_page.html'

#     def get(self, request):
#         records = instrument.objects.all()
#         create_form = Create_Instrument_Form(request.POST or None)
#         return Response({'create_form': create_form, 'records': records})


# class CreateInstrument(generics.CreateAPIView):
#     queryset = instrument.objects.filter(is_deleted= False) #We will just get the record that are not soft deleted
#     serializer_class = InstrumentSerializer
#     def post(self, request, *args, **kwargs):
#             form = Create_Instrument_Form(request.POST)
#             if form.is_valid():
#                 # Save the form data to the API
#                 response = super().post(request, *args, **kwargs)
#                 # Redirect to your desired URL after successful submission
#                 return response  # Adjust 'your-homepage-url' accordingly
#             return self.form_invalid(form)


# This is the API that will return records coming from the database. This Class if for integration purposes
#This view going to be able to create record for our api
#This will going to handle the query parameters so we can see all the records
# class InstrumentList(generics.ListCreateAPIView):
#     serializer_class = InstrumentSerializer

#     #queryset is the data that is going to be coming from the database
#     def get_queryset(self):
#         queryset = instrument.objects.select_related('accredbodies').filter(is_deleted= False) #We will just get the record that are not soft deleted
#         print(queryset)
#         return queryset
    

#     def post(self, request, *args, **kwargs):
#         serializer = InstrumentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             messages.success(request, f'Data successfully CREATED!') 
#             return redirect('accreditation:instrument-landing', status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class UpdateInstrument(generics.RetrieveUpdateAPIView):
#     queryset = instrument.objects.filter(is_deleted= False) #We will just get the record that are not soft deleted
#     serializer_class = InstrumentSerializer

    
# class ArchiveInstrument(generics.RetrieveUpdateAPIView):
#     serializer_class = InstrumentSerializer
#     queryset = instrument.objects.filter(is_deleted= False) #We will just get the record that are not soft deleted