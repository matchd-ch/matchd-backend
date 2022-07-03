from django import forms
from django.forms.models import model_to_dict

from db.exceptions import FormException
from db.models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, _ in self.fields.items():
            self.fields[key].required = False


def update_student_info(user, data):
    errors = {}

    student = user.student

    form_data = model_to_dict(student)
    form_data.update(data)

    form = StudentForm(form_data, instance=student)

    form.full_clean()

    if form.is_valid():
        student = form.save()
    else:
        errors.update(form.errors.get_json_data())
        raise FormException(errors=errors)

    return student
