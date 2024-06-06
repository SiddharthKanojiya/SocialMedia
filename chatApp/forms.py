from django import forms
from django.contrib.auth.models import User

from . import models

class GroupForm(forms.ModelForm):
    class Meta:
        model=models.Mygroup
        fields=['name','member']
        member = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )