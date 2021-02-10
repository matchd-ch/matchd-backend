from django import forms

from db.models import Student, UserLanguageRelation


class UserLanguageRelationForm(forms.ModelForm):
    class Meta:
        model = UserLanguageRelation
        fields = ('id', 'language', 'language_level', 'student')
