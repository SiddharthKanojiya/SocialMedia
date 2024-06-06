from django import forms
from django.contrib.auth.models import User
from . import models

class SignUpForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model=models.Profile
        fields=['dob','bio','profile_pic']
        widgets = {
    'dob': forms.DateInput(
        format=('%Y-%m-%d'),
        attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
              }),
}
        
class DweetForm(forms.ModelForm):
    class Meta:
        model=models.Dweet
        fields=['body','post','title']
        widgets = {
        'body': forms.Textarea(attrs={'rows': 3, 'cols': 30})
        }
        


class CommentForm(forms.Form):
    dweetid=  forms.CharField(max_length=20)
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))