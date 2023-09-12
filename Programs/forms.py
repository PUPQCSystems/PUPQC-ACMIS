from django import forms
from .models import Program

class CreateForm(forms.ModelForm):
    color_code = forms.CharField(widget=forms.TextInput(attrs={"type": "color", "style": "height: 37px"})) #Customizing the color code field
    class Meta:
        model = Program
        fields = ('program_name', 'abbreviation', 'description', 'color_code')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['color_code'].label = "Background Color" #Sets the label of Color Code into BG color
        