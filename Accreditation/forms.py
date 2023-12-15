from django import forms
from django.urls import reverse_lazy
from .models import accredtype, accredlevel, accredbodies, instrument, Programs, instrument_level
from .validators import name_validate, description_validate
from django.core.validators import RegexValidator

class Create_Type_Form(forms.ModelForm):
    name = forms.CharField(validators=[name_validate], max_length=20, required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={}), max_length=2000,  required=True)

    class Meta:
        model = accredtype
        fields = ('name', 'description')


class Create_Level_Form(forms.ModelForm):
    name = forms.CharField(max_length=20, required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={}), max_length=2000,  required=True)

    class Meta:
        model = accredlevel
        fields = ('name', 'description')


class Create_Bodies_Form(forms.ModelForm):
    name = forms.CharField(max_length=250, required=True)
    description = forms.Textarea()
    abbreviation = forms.CharField(label="Abbreviation", max_length=20, required=True)

    class Meta:
        model = accredbodies
        fields = ('name', 'abbreviation', 'description')

class Create_Instrument_Form(forms.ModelForm):
    name = forms.CharField(max_length=250, 
                           min_length = 5,
                           validators= [RegexValidator(r'^[a-zA-ZÁ-ÿ\s]*$', message="Only Letters are Allowed!")])
    description = forms.Textarea()
    accredbodies = forms.ModelChoiceField(
        label = "Accrediting Body", 
        queryset=accredbodies.objects.filter(is_deleted=False), 
        required=True, 
        empty_label="Select Accrediting Body")
    
    program = forms.ModelChoiceField(
        label = "Program", 
        queryset=Programs.objects.filter(is_deleted=False), 
        required=True, 
        empty_label="Select a Program")


    class Meta:
        model = instrument
        fields = ('name', 'accredbodies', 'program','description' )

    
class Create_InstrumentLevel_Form(forms.ModelForm):
    level = forms.ModelChoiceField(
        label = "Level", 
        queryset=accredlevel.objects.filter(is_deleted=False), 
        required=True, 
        empty_label="Select a Level")
    
    class Meta:
        model = instrument
        fields = ('level', 'description')

        widgets = {
            'description': forms.Textarea(attrs={'required': False}),
        }

