from django import forms

from db.models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('mobile_number', )
