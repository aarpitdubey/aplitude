from django import forms
from django.contrib.auth.models import User
from . import models
from assessment import models as CMODEL

class CandidateUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class CandidateForm(forms.ModelForm):
    class Meta:
        model=models.Candidate
        fields=['address','mobile','profile_pic']

