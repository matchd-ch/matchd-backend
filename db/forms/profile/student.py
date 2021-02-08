from django import forms
from django.conf import settings
from django.core.validators import RegexValidator, MinLengthValidator

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
    field_of_study = forms.CharField(max_length=255, required=True, validators=[MinLengthValidator(3)])
    graduation = forms.DateField(required=False)


class StudentProfileFormStep5(forms.Form):
    nickname = forms.CharField(max_length=150)


class StudentProfileFormStep6(forms.Form):
    state = forms.ChoiceField(choices=UserState.choices)
