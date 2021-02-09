from django import forms

from db.models import Distinction


class DistinctionForm(forms.ModelForm):
    class Meta:
        model = Distinction
        fields = ('id', 'text', 'student', )
