from django import forms
from django.conf import settings
from django.core.validators import RegexValidator

from db.models.user import UserState


class StudentProfileFormStep1(forms.Form):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    street = forms.CharField(max_length=255, required=True)
    zip = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=255, required=True)
    date_of_birth = forms.DateField(required=True)
    mobile = forms.CharField(max_length=12, validators=[RegexValidator(regex=settings.MOBILE_REGEX)], required=True)


class StudentProfileFormStep5(forms.Form):
    nickname = forms.CharField(max_length=150)


class StudentProfileFormStep6(forms.Form):
    state = forms.ChoiceField(choices=UserState.choices)
