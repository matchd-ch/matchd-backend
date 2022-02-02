from django import forms

from db.models import JobPostingLanguageRelation


class JobPostingLanguageRelationForm(forms.ModelForm):

    class Meta:
        model = JobPostingLanguageRelation
        fields = ('id', 'language', 'language_level', 'job_posting')
