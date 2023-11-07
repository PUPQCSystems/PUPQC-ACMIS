from django import forms
from .models import accredtype, accredlevel, accredbodies
from .validators import name_validate, description_validate

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

