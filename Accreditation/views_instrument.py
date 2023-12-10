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

# This is the API that will return records coming from the database. This Class if for integration purposes
#This view going to be able to create record for our api
#This will going to handle the query parameters so we can see all the records
class InstrumentList(generics.ListCreateAPIView):
    serializer_class = InstrumentSerializer

    #queryset is the data that is going to be coming from the database
    def get_queryset(self):
        queryset = instrument.objects.filter(is_deleted= False) #We will just get the record that are not soft deleted
        return queryset
    

    def post(self, request, *args, **kwargs):
        serializer = InstrumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateInstrument(generics.RetrieveUpdateAPIView):
    queryset = instrument.objects.filter(is_deleted= False) #We will just get the record that are not soft deleted
    serializer_class = InstrumentSerializer

   
class CreateInstrument(generics.CreateAPIView):
    queryset = instrument.objects.filter(is_deleted= False) #We will just get the record that are not soft deleted
    serializer_class = InstrumentSerializer

    def post(self, request, *args, **kwargs):
        serializer = InstrumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, f'Data successfully CREATED!') 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    

class ArchiveInstrument(generics.RetrieveUpdateAPIView):
    serializer_class = InstrumentSerializer
    queryset = instrument.objects.filter(is_deleted= False) #We will just get the record that are not soft deleted


#This function gets the list of data from the api and then load it to the html file
# This is a function that gets the data from the api and then show the data in html
def landing_page(request):
    records = requests.get('http://127.0.0.1:8000/accreditation/instrument/api/list/').json()
    create_form = Create_Instrument_Form(request.POST or None)
    context = {'create_form': create_form, 'records': records}
    return render(request, 'accreditation-instrument/landing_page.html', context)

def update_instrument(request, pk):
    # Assuming you have a form for updating instruments
    update_form = Create_Instrument_Form(request.POST or None)

    if request.method == 'PUT':
        # Validate the form
        if update_form.is_valid():
            # Get the data from the form
            data = update_form.cleaned_data

            # Make a PUT request to update the record using the API
            update_url = f'http://127.0.0.1:8000/accreditation/instrument/api/update/{pk}/'
            response = requests.put(update_url, data=data)

            if response.status_code == 200:
                # Successful update, you can redirect to a success page or do something else
                return redirect('success-page')
            else:
                # Handle the case when the update is not successful
                # You may want to provide error messages or log the error
                error_message = f"Failed to update the record. Status code: {response.status_code}"
                print(error_message)
                # You can include the error message in the context for rendering the form again
                context = {'update_form': update_form, 'error_message': error_message}
                return render(request, 'your_template.html', context)

    # Fetch the record data for pre-filling the form
    record_url = f'http://127.0.0.1:8000/accreditation/instrument/api/update/{pk}/'
    record = requests.get(record_url).json()

    # Pre-fill the form with the existing record data
    update_form = Create_Instrument_Form(initial=record)

    context = {'update_form': update_form}
    return render(request, 'your_template.html', context)


#------------------------------------------------------------[ VALIDATION ]------------------------------------------------------------#
def check_instru_name(request):
    create_form = Create_Instrument_Form(request.GET)
    return HttpResponse(as_crispy_field(create_form['name']))




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