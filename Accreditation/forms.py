from django import forms
from .models import accredtype
from .validators import name_validate, description_validate

class Create_Type_Form(forms.ModelForm):
    name = forms.CharField(validators=[name_validate], max_length=20, required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={}), max_length=2000,  required=True)

    class Meta:
        model = accredtype
        fields = ('name', 'description')

