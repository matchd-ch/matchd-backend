from django import forms
from django.conf import settings
from django.core.validators import RegexValidator, MinLengthValidator

from db.helper import convert_objects_to_id
from db.models import JobOption, JobPosition
from db.models.user import UserState


class StudentProfileFormStep1(forms.Form):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    street = forms.CharField(max_length=255, required=False)
    zip = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=255, required=False)
    date_of_birth = forms.DateField(required=True)
    mobile = forms.CharField(max_length=12, validators=[RegexValidator(regex=settings.MOBILE_REGEX)], required=False)


class StudentProfileFormStep2(forms.Form):
    school_name = forms.CharField(max_length=255, required=False)
    field_of_study = forms.CharField(max_length=255, required=False, validators=[MinLengthValidator(3)])
    graduation = forms.DateField(required=False)


class StudentProfileFormStep3(forms.Form):
    job_option = forms.ModelChoiceField(queryset=JobOption.objects.all(), required=True)
    job_position = forms.ModelChoiceField(queryset=JobPosition.objects.all(), required=False)

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data = convert_objects_to_id(data, 'job_option')
        data = convert_objects_to_id(data, 'job_position')
        super().__init__(data=data, **kwargs)


class StudentProfileFormStep3Date(forms.Form):
    job_from_date = forms.DateField(required=True)


class StudentProfileFormStep3DateRange(forms.Form):
    job_from_date = forms.DateField(required=True)
    job_to_date = forms.DateField(required=True)


class StudentProfileFormStep5(forms.Form):
    nickname = forms.CharField(max_length=150)


class StudentProfileFormStep6(forms.Form):
    state = forms.ChoiceField(choices=UserState.choices)
