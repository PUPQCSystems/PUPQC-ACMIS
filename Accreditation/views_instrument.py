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


class InstrumentList(View):
    def get(self, request):
        #Getting the data from the API
        instrument_form = Create_Instrument_Form(request.POST or None)
        instrumentlevel_form = Create_InstrumentLevel_Form(request.POST or None)
        records =instrument.objects.select_related('accredbodies').filter(is_deleted= False) #Getting all the data inside the Program table and storing it to the context variable

        # Initialize an empty list to store update forms for each record
        details = []

        # Iterate through each record and create an update form for it
        for record in records:
            update_form = Create_Instrument_Form(instance=record)
            created_by = record.created_by  # Get the user who created the record
            modified_by = record.modified_by  # Get the user who modified the record
            details.append((record, update_form, created_by, modified_by))
            
        context = { 'records': records, 'instrument_form': instrument_form, 'details': details, 'instrumentlevel_form':  instrumentlevel_form }  #Getting all the data inside the type table and storing it to the context variable

        return render(request, 'accreditation-instrument/main-page/landing_page.html', context)
    
    def post(self, request):
        instrument_form = Create_Instrument_Form(request.POST or None)

        if instrument_form.is_valid():
            instrument_form.instance.created_by = request.user
            instrument_form.save()
            name = instrument_form.cleaned_data.get('name')
            messages.success(request, f'{name} accreditation instrument is successfully created!') 
            # url_landing = "{% url 'accreditations:type' %}"
            url_landing = "/accreditation/instrument/"
            return JsonResponse({'url_landing': url_landing}, status=201)
        else:
            # Return a validation error using a JSON response
            return JsonResponse({'errors': instrument_form.errors}, status=400)
        
   
@login_required
def update(request, pk):
# Retrieve the type object with the given primary key (pk)
    try:
        accreditation_instrument = instrument.objects.get(id=pk)
    except instrument.DoesNotExist:
        return JsonResponse({'errors': 'instrument not found'}, status=404)

    if request.method == 'POST':
        # Process the form submission with updated data
        update_form = Create_Instrument_Form(request.POST or None, instance=accreditation_instrument)
        if update_form.is_valid():
            # Save the updated data to the database
            update_form.instance.modified_by = request.user
            update_form.save()  
            name = update_form.cleaned_data.get('name')

            # Provide a success message as a JSON response
            messages.success(request, f'{name} is successfully updated!') 
            return JsonResponse({'status': 'success'}, status=200)


        else:
            # Return a validation error as a JSON response
            return JsonResponse({'errors': update_form.errors}, status=400)
        
@login_required
def archive(request, pk):
    # Gets the records who have this ID
    accreditation_instrument = instrument.objects.get(id=pk)

    #After getting that record, this code will delete it.
    accreditation_instrument.modified_by = request.user
    accreditation_instrument.is_deleted=True
    accreditation_instrument.deleted_at = timezone.now()
    name = accreditation_instrument.name
    accreditation_instrument.save()
    messages.success(request, f'{name} accreditation instrument is successfully archived!') 
    return redirect('accreditations:instrument-list')

#------------------------------------------------------------[ ARCHIVE PAGE CODES ]------------------------------------------------------------#
@login_required
def archive_landing(request):
    records =instrument.objects.select_related('accredbodies').filter(is_deleted= True) #Getting all th

    details = []
     # Iterate through each record and create an update form for it
    for record in records:
        update_form = Create_Instrument_Form(instance=record)
        created_by = record.created_by  # Get the user who created the record
        modified_by = record.modified_by  # Get the user who modified the record
        details.append((record, update_form,created_by, modified_by))

    context = { 'details': details }#Getting all the data inside the type table and storing it to the context variable
    return render(request, 'accreditation-instrument/archive-page/landing-page.html', context)

@login_required
def restore(request, pk):
    # Gets the records who have this ID
    accreditation_instrument = instrument.objects.get(id=pk)

    #After getting that record, this code will restore it.
    accreditation_instrument.modified_by = request.user
    accreditation_instrument.deleted_at = None
    accreditation_instrument.is_deleted=False
    name = accreditation_instrument.name
    accreditation_instrument.save()
    messages.success(request, f'{name} accreditation level is successfully restored!') 
    return redirect('accreditations:instrument-archive-page')

@login_required
def destroy(request, pk):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user

        if user and user.is_authenticated:
            if authenticate(email=user.email, password=entered_password):
                # Gets the records who have this ID
                accreditation_instrument = instrument.objects.get(id=pk)

                #After getting that record, this code will delete it.
                accreditation_instrument.delete()
                messages.success(request, f'Accreditation Level is permanently deleted!') 
                url_landing = "/accreditation/instrument/archive_page/"
                return JsonResponse({'success': True, 'url_landing': url_landing}, status=200)
            
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect password'})
        else:
            return JsonResponse({'success': False, 'error': 'User not logged in'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


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