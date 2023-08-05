from django import forms
from .models import Resume,Job

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['first_name', 'last_name', 'linkdean', 'pdf']

class Cform(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'j_description', 'skills', 'offer', 'location', 'no_of_opening']
