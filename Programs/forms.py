from django import forms
from .models import Programs
from .validators import program_name_validate

class CreateForm(forms.ModelForm):
    program_name = forms.CharField(validators=[program_name_validate], required=True)
    abbreviation = forms.CharField(label="Abbreviation", max_length=10, required=True)
    description = forms.Textarea()

    def clean(self):
        cleaned_data = super().clean()

        # Convert 'program_name' and 'abbreviation' to uppercase
        if 'program_name' in cleaned_data:
            cleaned_data['program_name'] = cleaned_data['program_name'].upper()

        if 'abbreviation' in cleaned_data:
            cleaned_data['abbreviation'] = cleaned_data['abbreviation'].upper()

        return cleaned_data

    class Meta:
        model = Programs
        fields = ('program_name', 'abbreviation', 'description')

        widgets = {
            'description': forms.Textarea(attrs={'required': False}),
        }




    

        
        