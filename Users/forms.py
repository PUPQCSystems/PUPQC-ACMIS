from django import forms
from Users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'id': 'validationCustom01'})
    )

    first_name = forms.CharField(
        max_length=150, required=True,
        widget=forms.TextInput(attrs={'id': 'validationCustom02'})
    )
    last_name = forms.CharField(
        max_length=150, required=True,
        widget=forms.TextInput(attrs={'id': 'validationCustom03'})
    )

    middle_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = CustomUser
        fields = ('email' ,'password1', 'password2','first_name', 'last_name', 'middle_name')

# This is a form validation for the registration form
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = CustomUser.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} is already in use.")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize help_texts for password input field
        self.fields['password1'].help_text = (
            "Your password must meet the following criteria:"
            "<ul>"
                "<li>Can’t be too similar to your other personal information.</li>"
                "<li>Must contain at least 8 characters.</li>"
                "<li>Can’t be a commonly used password.</li>"
                "<li>Can’t be entirely numeric.</li>"
            "</ul>"
        )

class UpdateForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'id': 'validationCustom01'})
    )

    first_name = forms.CharField(
        max_length=150, required=True,
        widget=forms.TextInput(attrs={'id': 'validationCustom02'})
    )
    last_name = forms.CharField(
        max_length=150, required=True,
        widget=forms.TextInput(attrs={'id': 'validationCustom03'})
    )

    middle_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = CustomUser
        fields = ('email','first_name', 'last_name', 'middle_name')

    def clean_email(self):
        current_email = self.instance.email
        new_email = self.cleaned_data['email'].lower()

        # Check if email has been changed
        if current_email != new_email:
            try:
                account = CustomUser.objects.get(email=new_email)
                raise forms.ValidationError(f"Email {new_email} is already in use.")
            except Exception as e:
                pass

        return new_email
