from django import forms

from db.exceptions import FormException
from db.models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('is_matchable', )


def update_student_info(user, data):
    errors = {}

    student = user.student

    form = StudentForm(data, instance=student)

    form.full_clean()

    if form.is_valid():
        student = form.save()
    else:
        errors.update(form.errors.get_json_data())
        raise FormException(errors=errors)

    return student
