from django import forms
from .models import Programs
from .validators import program_name_validate, abbreviation_validate, description_validate

class CreateForm(forms.ModelForm):
    program_name = forms.CharField(validators=[program_name_validate])
    description = forms.Textarea()
    abbreviation = forms.CharField(label="Abbreviation", max_length=10, required=True)

    class Meta:
        model = Programs
        fields = ('program_name', 'abbreviation', 'description')

    

        
        