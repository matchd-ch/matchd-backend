from django import forms
from django.conf import settings
from django.core.validators import RegexValidator
from django.forms import formset_factory

from db.forms import HobbyForm
from db.models import Skill, Hobby


class StudentProfileFormStep4(forms.Form):
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all())
    # hobbies = forms.CharField(max_length=150)
    # distinctions = forms.CharField(max_length=100)
    # online_projects = forms.CharField(max_length=255)
    # languages = forms.CharField(max_length=255, required=True)
