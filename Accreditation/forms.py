from django import forms
from django.forms import ValidationError, modelformset_factory
from django.urls import reverse_lazy
from .models import *
from .validators import name_validate, description_validate
from django.core.validators import RegexValidator
import re


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
        fields = ('name',)


class Component_Form(forms.ModelForm):
    name = forms.CharField(
        max_length=100, 
        min_length = 5,
        required=True, 
        error_messages={'required': "Please enter a component name before submitting the form."},
        validators= [RegexValidator(r'^[a-zA-ZÁ-ÿ0-9\s\'&()/-]*$', 
                            message="Only Letters, Numbers, Apostrophe, Hyphen, Ampersand, and Parentheses are allowed in the Name Field!")]
                            )
    description = forms.CharField(widget=forms.Textarea(attrs={}), max_length=2000,  required=False)

    class Meta:
        model = components
        fields = ('name', 'description')

    def clean(self):
        cleaned_data = super().clean()
        
        # Ensure 'name' is present before trying to access it
        if 'name' in cleaned_data:
            cleaned_data['name'] = cleaned_data['name'].upper()  # Convert to uppercase

        return cleaned_data
    
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


# class Create_InstrumentDirectory_Form(forms.ModelForm):
#     name = forms.CharField(
#         label = "Name", 
#         required=True, 
#         error_messages={'required': "Please enter a name before submitting the form."})
    
#     class Meta:
#         model = instrument_level_folder
#         fields = ('name',)


class Create_InstrumentDirectory_Form(forms.ModelForm):
    name = forms.CharField(
        label = "Name", 
        required=True, 
        validators= [RegexValidator(r'^[a-zA-ZÁ-ÿ\s.,\'()&0-9]*$', 
        message="Only Letters, Numbers, Decimal Point, Comma, Apostrophe, Ampersand, and Parentheses are allowed in the Name Field!")],
        error_messages={'required': "Please enter a name before submitting the form."})

    # Use BooleanField for checkbox fields
    has_progress_bar = forms.BooleanField(
        label="Has Progress Bar",
        required=False
    )
    
    has_assign_button = forms.BooleanField(
        label="Has Assign Button",
        required=False
    )

    due_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 
                                                                        'class': 'form-control'}),
                                                                        required=False,)
    
    class Meta:
        model = instrument_level_folder
        fields = ('name', 'label','due_date', 'description', 'has_progress_bar', 'has_assign_button')

class SubmissionBin_Form(forms.ModelForm):
    name = forms.CharField(max_length=500, 
                           min_length = 5, 
                           required=True,
                            validators= [RegexValidator(r'^[a-zA-ZÁ-ÿ\s.,\'()&0-9]*$', 
                            message="Only Letters, Numbers, Decimal Point, Comma, Apostrophe, Ampersand, and Parentheses are allowed in the Name Field!")],
                            error_messages={'required': "Please enter a name before submitting the form."})

    class Meta:
        model = instrument_level_folder
        fields = ('name', 'description')

        widgets = {
            'description': forms.Textarea(attrs={'required': False,
                                                 'max_length': 2000,
                                                 'min_length': 5,
                                                 'validators': [RegexValidator(r'^[a-zA-ZÁ-ÿ\s.,\'()&0-9]*$', 
                                                    message="Only Letters, Numbers, Decimal Point, Comma, Apostrophe, Ampersand, and Parentheses are allowed in the Description Field!")]
                                                    }),
        }