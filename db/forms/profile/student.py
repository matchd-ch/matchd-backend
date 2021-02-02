from django import forms

from db.models.user import UserState


class StudentProfileStep6Form(forms.Form):
    state = forms.ChoiceField(choices=UserState.choices)
