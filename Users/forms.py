from django import forms
from Users.models import CustomUser, CustomUser_profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, Permission
from django.core.validators import RegexValidator

class CreateUserForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email' ,'password1', 'password2','first_name', 'last_name', 'middle_name')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control textinput',
                                    'id': 'reg_first_name_id',
                                    'max_length':150, 
                                    'min_length' : 5,
                                    'required':True, 
                                    'validators': [RegexValidator(r'^[a-zA-ZÁ-ÿ\s.,\'()&]*$', 
                                                                message="Only Letters, Decimal Point, Comma, Apostrophe, Ampersand, and Parentheses are allowed in the first name Field!")],
                                    'error_messages': {'required': "Please enter a name before submitting the form."}}),
            'last_name': forms.TextInput(attrs={'class': 'form-control textinput',
                                    'id': 'reg_last_name_id',
                                    'max_length':50, 
                                    'min_length' : 5,
                                    'required':True, 
                                    'validators': [RegexValidator(r'^[a-zA-ZÁ-ÿ\s.,\'()&]*$', 
                                                                message="Only Letters, Decimal Point, Comma, Apostrophe, Ampersand, and Parentheses are allowed in the last name Field!")],
                                    'error_messages': {'required': "Please enter a name before submitting the form."}}),

            'middle_name': forms.TextInput(attrs={'class': 'form-control textinput',
                                    'id': 'reg_middle_name_id',
                                    'max_length':150, 
                                    'min_length' : 5,
                                    'required':False, 
                                    'validators': [RegexValidator(r'^[a-zA-ZÁ-ÿ\s.,\'()&]*$', 
                                                                message="Only Letters, Decimal Point, Comma, Apostrophe, Ampersand, and Parentheses are allowed in the middle name Field!")],
                                   }),

            'password1': forms.PasswordInput(attrs={'class': 'form-control',
                                                     'id': 'reg_password1_id',
                                                'max_length':50, 
                                                'min_length' : 5,
                                                'required':True, 
                                                'validators': [RegexValidator(r'^[a-zA-ZÁ-ÿ\s.,\'()&]*$', 
                                                                            message="Only Letters, Decimal Point, Comma, Apostrophe, Ampersand, and Parentheses are allowed in the Label Field!")],
                                               }),


            'password1': forms.PasswordInput(attrs={'class': 'form-control',
                                                     'id': 'reg_password1_id',
                                                'max_length':50, 
                                                'min_length' : 5,
                                                'required':True, 
                                                'validators': [RegexValidator(r'^[a-zA-ZÁ-ÿ\s.,\'()&]*$', 
                                                                            message="Only Letters, Decimal Point, Comma, Apostrophe, Ampersand, and Parentheses are allowed in the Label Field!")],
                                                }),

            'email': forms.EmailInput(attrs={'class': 'form-control',
                                                     'id': 'reg_email_id',
                                                'max_length':50, 
                                                'min_length' : 5,
                                                'required':True, 
                                                'validators': [RegexValidator(r'^[a-zA-ZÁ-ÿ\s.,\'()&]*$', 
                                                                            message="Only Letters, Decimal Point, Comma, Apostrophe, Ampersand, and Parentheses are allowed in the Label Field!")],
                                                }),

            }

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
    class Meta:
        model = CustomUser
        fields = ('email','first_name', 'last_name', 'middle_name')

        widgets = {
                    'first_name': forms.TextInput(attrs={'class': 'form-control textinput',
                                            'id': 'first_name_id',
                                            'max_length':150, 
                                            'min_length' : 5,
                                            'required':True, 
                                            'validators': [RegexValidator(r'^[a-zA-ZÁ-ÿ\s.,\'()&]*$', 
                                                                        message="Only Letters, Decimal Point, Comma, Apostrophe, Ampersand, and Parentheses are allowed in the first name Field!")],
                                            'error_messages': {'required': "Please enter a name before submitting the form."}}),
                    'last_name': forms.TextInput(attrs={'class': 'form-control textinput',
                                            'id': 'last_name_id',
                                            'max_length':50, 
                                            'min_length' : 5,
                                            'required':True, 
                                            'validators': [RegexValidator(r'^[a-zA-ZÁ-ÿ\s.,\'()&]*$', 
                                                                        message="Only Letters, Decimal Point, Comma, Apostrophe, Ampersand, and Parentheses are allowed in the last name Field!")],
                                            'error_messages': {'required': "Please enter a name before submitting the form."}}),

                    'middle_name': forms.TextInput(attrs={'class': 'form-control textinput',
                                            'id': 'middle_name_id',
                                            'max_length':150, 
                                            'min_length' : 5,
                                            'required':False, 
                                            'validators': [RegexValidator(r'^[a-zA-ZÁ-ÿ\s.,\'()&]*$', 
                                                                        message="Only Letters, Decimal Point, Comma, Apostrophe, Ampersand, and Parentheses are allowed in the middle name Field!")],
                                            }),
                            }

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


class ProfilePicForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('profile_pic',)


class AuthGroup_Form(forms.ModelForm):
    
    class Meta:
        model = Group
        fields = ('name', )

        widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control textinput',
                                'max_length':50, 
                                'min_length' : 5,
                                'required':True, 
                                'validators': [RegexValidator(r'^[a-zA-ZÁ-ÿ\s.,\'()&]*$', 
                                                            message="Only Letters, Decimal Point, Comma, Apostrophe, Ampersand, and Parentheses are allowed in the Label Field!")],
                                'error_messages': {'required': "Please enter a name before submitting the form."}}),
        }
