from django import forms
from Users.models import NewUser

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = NewUser
        fields = ('email', 'password')


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=150,required=True)

    last_name = forms.CharField(max_length=150,required=True)
    middle_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = NewUser
        fields = ('email', 'password', 'first_name', 'last_name', 'middle_name')


