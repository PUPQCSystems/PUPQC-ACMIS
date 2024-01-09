from django import forms
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from .models import *
from .validators import name_validate, description_validate
from django.core.validators import RegexValidator
import re

class Create_Type_Form(forms.ModelForm):
    name = forms.CharField( validators=[name_validate], max_length=20, required=True,
                            error_messages={'required': "Please enter a name before submitting the form."})
    description = forms.CharField(widget=forms.Textarea(attrs={}), max_length=2000,  required=False)

    class Meta:
        model = accredtype
        fields = ('name', 'description')

    def clean(self):
        cleaned_data = super().clean()

        # Convert 'name' and 'abbreviation' to uppercase
        if 'name' in cleaned_data:
            cleaned_data['name'] = cleaned_data['name'].upper()


        return cleaned_data


class Create_Level_Form(forms.ModelForm):
    name = forms.CharField(max_length=20, required=True,
                           error_messages={'required': "Please enter a name before submitting the form."})
    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Define the regular expression pattern for the allowed formats
        allowed_formats = re.compile(r'^(Level\s+[IVXLCDM]+|[IVXLCDM]+)$', re.IGNORECASE)

        if not allowed_formats.match(name):
            raise forms.ValidationError('Invalid format. Please only use the "Level" word and followed by Roman numerals (e.g., IV, V) to create a Level. For example "Level IX" or "level ix')

        return name


    def clean(self):
        cleaned_data = super().clean()
        
        # Ensure 'name' is present before trying to access it
        if 'name' in cleaned_data:
            cleaned_data['name'] = cleaned_data['name'].upper()  # Convert to uppercase

        return cleaned_data

    class Meta:
        model = accredlevel
        fields = ['name']


class Create_Area_Form(forms.ModelForm):
    area_number = forms.CharField(max_length=10, required=True,
                                  error_messages={'required': "Please enter an area number before submitting the form."})

    def clean_area_number(self):
        area_number = self.cleaned_data.get('area_number')

        # Define the regular expression pattern for the allowed formats
        allowed_formats = re.compile(r'^(Area\s+[IVXLCDM]+|[IVXLCDM]+)$', re.IGNORECASE)

        if not allowed_formats.match(area_number):
            raise forms.ValidationError('Invalid format. Please only use the "Area" word and Roman numerals (e.g., IV, V) to create an Area. For example "Area IX" or "area ix')

        return area_number


    def clean(self):
        cleaned_data = super().clean()
        
        # Ensure 'area_number' is present before trying to access it
        if 'area_number' in cleaned_data:
            cleaned_data['area_number'] = cleaned_data['area_number'].upper()  # Convert to uppercase

        return cleaned_data
    
    class Meta:
        model = area
        fields = ['area_number']

class Parameter_Form(forms.ModelForm):
    name = forms.CharField(max_length=20, required=True,
                                  error_messages={'required': "Please enter a parameter name before submitting the form."})

    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Define the regular expression pattern for the allowed formats
        allowed_formats = re.compile(r'^Parameter [A-Za-z]$', re.IGNORECASE)

        if not allowed_formats.match(name):
            raise forms.ValidationError('Invalid format. Please only use the "Parameter" word and followed by letter (e.g., A, C, G) to create a Parameter. For example "Parameter A" or "parameter b')

        return name


    def clean(self):
        cleaned_data = super().clean()
        
        # Ensure 'name' is present before trying to access it
        if 'name' in cleaned_data:
            cleaned_data['name'] = cleaned_data['name'].upper()  # Convert to uppercase

        return cleaned_data
    
    class Meta:
        model = parameter
        fields = ['name']


class Create_Bodies_Form(forms.ModelForm):
    name = forms.CharField( max_length=250, required=True,
                            error_messages={'required': "Please enter a name before submitting the form."})
    description = forms.CharField(widget=forms.Textarea(attrs={}), max_length=2000,  required=False)
    abbreviation = forms.CharField(label="Abbreviation", max_length=20, required=True,
                                   error_messages={'required': "Please enter an abbreviation before submitting the form."})

    class Meta:
        model = accredbodies
        fields = ('name', 'abbreviation', 'description')

    def clean(self):
        cleaned_data = super().clean()

        # Convert 'program_name' and 'abbreviation' to uppercase
        if 'name' in cleaned_data:
            cleaned_data['name'] = cleaned_data['name'].upper()

        if 'abbreviation' in cleaned_data:
            cleaned_data['abbreviation'] = cleaned_data['abbreviation'].upper()

        return cleaned_data
    


class Create_Instrument_Form(forms.ModelForm):
    name = forms.CharField(max_length=250, 
                           min_length = 5,
                           validators= [RegexValidator(r'^[a-zA-ZÁ-ÿ\s]*$', message="Only Letters are Allowed!")],
                            error_messages={'required': "Please enter a name before submitting the form."})
    description = forms.CharField(widget=forms.Textarea(attrs={}), max_length=5000,  required=False)
    accredbodies = forms.ModelChoiceField(
        label = "Accrediting Body", 
        queryset=accredbodies.objects.filter(is_deleted=False), 
        required=True, 
        empty_label="Select Accrediting Body",
        error_messages={'required': "Please select an accrediting body before submitting the form."})
    
    program = forms.ModelChoiceField(
        label = "Program", 
        queryset=Programs.objects.filter(is_deleted=False), 
        required=True, 
        empty_label="Select a Program",
        error_messages={'required': "Please select a program before submitting the form."})
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Ensure 'name' is present before trying to access it
        if 'name' in cleaned_data:
            cleaned_data['name'] = cleaned_data['name'].upper()  # Convert to uppercase

        return cleaned_data

    class Meta:
        model = instrument
        fields = ('name', 'accredbodies', 'program','description')

        widgets = {
            'description': forms.Textarea(attrs={'required': False}),
        }


class Create_InstrumentLevel_Form(forms.ModelForm):
    level = forms.ModelChoiceField(
        label = "Level", 
        queryset=accredlevel.objects.filter(is_deleted=False), 
        required=True, 
        empty_label="Select a Level",
        error_messages={'required': "Please select a level before submitting the form."})
    
    class Meta:
        model = instrument_level
        fields = ('level', 'description')

        widgets = {
            'description': forms.Textarea(attrs={'required': False}),
        }


class Create_LevelArea_Form(forms.ModelForm):
    area = forms.ModelChoiceField(
        label = "Area", 
        queryset = area.objects.filter(is_deleted=False), 
        required=True, 
        empty_label="Select an Area",
        error_messages={'required': "Please select an area number before submitting the form."})
    
    label = forms.CharField(
        max_length=250, 
        min_length = 5,
        required=False, 
        validators= [RegexValidator(r'^[a-zA-ZÁ-ÿ\s.,\'()&]*$', 
                                    message="Only Letters, Decimal Point, Comma, Apostrophe, Ampersand, and Parentheses are Allowed!")])
    
    description = forms.Textarea()
    
    class Meta:
        model = instrument_level_area
        fields = ('area', 'label','description')

        widgets = {
            'description': forms.Textarea(attrs={'required': False}),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # Ensure 'label' is present before trying to access it
        if 'label' in cleaned_data:
            cleaned_data['label'] = cleaned_data['label'].upper()  # Convert to uppercase

        return cleaned_data

LevelAreaFormSet = modelformset_factory(
    instrument_level_area, form=Create_LevelArea_Form, extra=1
)



class AreaParameter_Form(forms.ModelForm):
    parameter = forms.ModelChoiceField(
        label = "Parameter", 
        queryset = parameter.objects.filter(is_deleted=False), 
        required=True, 
        empty_label="Select an Area",
        error_messages={'required': "Please select a parameter before submitting the form."})
    
    label = forms.CharField(
        max_length=250, 
        min_length = 5,
        required=False, 
        validators= [RegexValidator(r'^[a-zA-ZÁ-ÿ\s.,\'()&]*$', 
                                    message="Only Letters, Decimal Point, Comma, Apostrophe, Ampersand, and Parentheses are Allowed!")])
    
    description = forms.Textarea()
    
    class Meta:
        model = instrument_level_area
        fields = ('parameter', 'label','description')

        widgets = {
            'description': forms.Textarea(attrs={'required': False}),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # Ensure 'label' is present before trying to access it
        if 'label' in cleaned_data:
            cleaned_data['label'] = cleaned_data['label'].upper()  # Convert to uppercase

        return cleaned_data

AreaParameterFormSet = modelformset_factory(
    level_area_parameter, form=AreaParameter_Form, extra=1
)