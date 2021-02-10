from django import forms
from db.models import Skill


class StudentProfileFormStep4(forms.Form):
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=True)
    # hobbies = forms.CharField(max_length=150)
    # distinctions = forms.CharField(max_length=100)
    # online_projects = forms.CharField(max_length=255)
    # languages = forms.CharField(max_length=255, required=True)
