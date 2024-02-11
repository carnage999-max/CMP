from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = [
            'email', 'student_tag', 'first_name',
            'last_name', 'middle_name', 'department', 'level', 'matric_number',
            'password1', 'password2'
        ]


class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
