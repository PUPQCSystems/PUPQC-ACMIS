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
        error_messages={'required': "Please enter a name before submitting the form."},
        widget=forms.TextInput(attrs={'class': 'form-control'}),)

    # Use BooleanField for checkbox fields
    has_progress_bar = forms.BooleanField(
        label="Has Progress Bar",
        required=False
    )
    
    has_assign_button = forms.BooleanField(
        label="Has Assign Button",
        required=False
    )

    can_be_reviewed = forms.BooleanField(
        label="Can be reviewed by the Reviewer",
        required=False
    )

    due_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 
                                                                        'class': 'form-control'}),
                                                                        required=False,)
    
    class Meta:
        model = instrument_level_folder
        fields = ('name', 'label','due_date', 'description', 'has_progress_bar', 'has_assign_button', 'can_be_reviewed')


    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get('due_date')

        if due_date:
            if due_date < timezone.now():
                raise ValidationError("Due Date should be set in the future.")

        return cleaned_data

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

# ---------------------------- [ PROGRAM ACCREDITATION FORM] ----------------------------
class ProgramAccreditation_Form(forms.ModelForm):
    program = forms.ModelChoiceField(
        label = "Program", 
        queryset= Programs.objects.filter(is_deleted=False), 
        required=True, 
        empty_label="Select a Program",
        error_messages={'required': "Please select a level before submitting the form."},
        widget=forms.Select(attrs={'class': 'form-control form-select select'}))
    
    instrument_level = forms.ModelChoiceField(
        label = "Instrument Level", 
        queryset= instrument_level.objects.filter(is_deleted=False), 
        required=True, 
        empty_label="Select an Instrument Level",
        error_messages={'required': "Please select an Instrument Level before submitting the form."},
        widget=forms.Select(attrs={'class': 'form-control form-select select'}))
    
    mock_accred_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 
                                                                     'class': 'form-control'}),
                                                                       required=True,
                                                                        error_messages={'required': "Please set the mock accreditation date beefore submitting the form."})
    
    
    survey_visit_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 
                                                                     'class': 'form-control'}), 
                                                                     required=True,
                                                                      error_messages={'required': "Please set the survey visit date before submitting the form."})

    class Meta:
        model = program_accreditation
        fields = ('program', 'instrument_level', 'mock_accred_date', 'survey_visit_date', 'description')

        widgets = {
            'description': forms.Textarea(attrs={'required': False, 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        mock_accred_date = cleaned_data.get('mock_accred_date')
        survey_visit_date = cleaned_data.get('survey_visit_date')

        if not survey_visit_date:
            raise ValidationError("Please set the survey visit date before submitting the form. ")

        if mock_accred_date and survey_visit_date:
            # Check if mock_accred_date is equal to survey_visit_date
            if mock_accred_date == survey_visit_date:
                raise ValidationError("Mock Accreditation Date cannot be equal to the survey visit date. ")

            # Check if mock_accred_date is after survey_visit_date
            if mock_accred_date > survey_visit_date:
                raise ValidationError("Mock Accreditation Date cannot be after the survey visit date. ")

            # Check if mock_accred_date is before the current date
            if mock_accred_date < timezone.now():
                raise ValidationError("Mock Accreditation Date should be set in the future. ")

        return cleaned_data
    

class ProgramAccreditation_UpdateForm(forms.ModelForm):
    program = forms.ModelChoiceField(
        label = "Program", 
        queryset= Programs.objects.filter(is_deleted=False), 
        required=True, 
        empty_label="Select a Program",
        error_messages={'required': "Please select a level before submitting the form."},
        widget=forms.Select(attrs={'class': 'form-control form-select select edit-select-button',
                               'id': 'id_program_update'}))
    
    instrument_level = forms.ModelChoiceField(
        label = "Instrument Level", 
        queryset= instrument_level.objects.filter(is_deleted=False), 
        required=True, 
        empty_label="Select an Instrument Level",
        error_messages={'required': "Please select an Instrument Level before submitting the form."},
        widget=forms.Select(attrs={'class': 'form-control form-select select edit-instrument-button',
                                    'id': 'id_instrument_level_update'}))
    
    mock_accred_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 
                                                                     'class': 'form-control'}),
                                                                       required=True,
                                                                        error_messages={'required': "Please set the mock accreditation date beefore submitting the form."})
    survey_visit_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 
                                                                     'class': 'form-control'}), 
                                                                     required=True,
                                                                      error_messages={'required': "Please set the survey visit date before submitting the form."})

    class Meta:
        model = program_accreditation
        fields = ('program', 'instrument_level', 'mock_accred_date', 'survey_visit_date', 'description')

        widgets = {
            'description': forms.Textarea(attrs={'required': False, 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        mock_accred_date = cleaned_data.get('mock_accred_date')
        survey_visit_date = cleaned_data.get('survey_visit_date')

        if not survey_visit_date:
            raise ValidationError("Please set the survey visit date before submitting the form. ")

        if mock_accred_date and survey_visit_date:
            # Check if mock_accred_date is equal to survey_visit_date
            if mock_accred_date == survey_visit_date:
                raise ValidationError("Mock Accreditation Date cannot be equal to the survey visit date. ")

            # Check if mock_accred_date is after survey_visit_date
            if mock_accred_date > survey_visit_date:
                raise ValidationError("Mock Accreditation Date cannot be after the survey visit date. ")

            # Check if mock_accred_date is before the current date
            if mock_accred_date < timezone.now():
                raise ValidationError("Mock Accreditation Date should be set in the future. ")

        return cleaned_data
    

# ---------------------------- [ REVIEW UPLOAD BIN FORM ] ---------------------------- #
class ReviewUploadBin_Form(forms.ModelForm):
    STATUS_CHOICES = [
            ('approve', 'Approve'), 
            ('rfr', 'Request for Resubmission')
        ]   
    
    status = forms.ChoiceField(
        label = "Status", 
        choices = STATUS_CHOICES,
        required = True, 
        error_messages={'required': "Please select a status before submitting the form."},
        widget=forms.Select(attrs={'class': 'form-control form-select select'}))


    
    class Meta:
        model = instrument_level_folder
        fields = ('status', 'remarks')

    widgets = {
        'remarks': forms.Textarea(attrs={'required': False}),
        }


# ---------------------------- [ File Upload FORM ] ---------------------------- #
class FileUpload_Form(forms.ModelForm):
   class Meta:
        model = files
        fields = ('file_path',)
        widgets = {
            'file_path': forms.FileInput(attrs={'id': 'file-path-{{ upload_bin.id }}'}),
        }



# ---------------------------- [ AREA ASSIGNMENT FORM ] ---------------------------- #
class ChairManAssignedToFolder_Form(forms.ModelForm):
    class Meta:
        model = user_assigned_to_folder
        fields = ['parent_directory', 'is_chairman']


class CoChairUserAssignedToFolder_Form(forms.ModelForm):
    class Meta:
        model = user_assigned_to_folder
        fields = ['parent_directory', 'is_cochairman']

class MemberAssignedToFolder_Form(forms.ModelForm):
    class Meta:
        model = user_assigned_to_folder
        fields = ['parent_directory','is_member']


# ---------------------------- [ ACCREDITATION RESULT FORMS ] ---------------------------- #

class PassedResult_Form(forms.ModelForm):
    validity_date_from = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 
                                                                     'class': 'form-control'}),
                                                                       required=True,
                                                                        error_messages={'required': "Please set the validity date 'from' before submitting the form."})
    validity_date_to = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 
                                                                     'class': 'form-control'}), 
                                                                     required=True,
                                                                      error_messages={'required': "Please set the validity date 'to' before submitting the form."})

    class Meta:
        model = program_accreditation
        fields = ('validity_date_from', 'validity_date_to')

    def clean(self):
        cleaned_data = super().clean()
        validity_date_from = cleaned_data.get('validity_date_from')
        validity_date_to = cleaned_data.get('validity_date_to')

        if  validity_date_from and  validity_date_to:
            # Check if  validity_date_from is equal to  validity_date_to
            if  validity_date_from ==  validity_date_to:
                raise ValidationError("Validity Date 'from' cannot be equal to the survey visit date. ")

            # Check if  validity_date_from is after  validity_date_to
            if  validity_date_from >  validity_date_to:
                raise ValidationError("Validity Date 'from' cannot be after the survey visit date. ")

            # Check if  validity_date_from is before the current date
            if  validity_date_from < timezone.now():
                raise ValidationError("Validity Date 'from' should be set in the future. ")

        return cleaned_data

class RevisitResult_Form(forms.ModelForm):
    revisit_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 
                                                                     'class': 'form-control'}),
                                                                       required=True,
                                                                        error_messages={'required': "Please set the mock accreditation date beefore submitting the form."})

    class Meta:
        model = program_accreditation
        fields = ('revisit_date',)



    def clean(self):
        cleaned_data = super().clean()
        revisit_date = cleaned_data.get('revisit_date')

        if not revisit_date:
            raise ValidationError("Please ensure that the survey revisit date is set before submitting the form.")

        if revisit_date:
            if revisit_date < timezone.now():
                raise ValidationError("Revisit Date should be set in the future. ")

        return cleaned_data
    

class RemarksResult_Form(forms.ModelForm):
    class Meta:
        model = result_remarks
        fields = ('remarks',)
        widgets = {
            'remarks': forms.Textarea(attrs={'required': False, 'class': 'form-control'}),
        }