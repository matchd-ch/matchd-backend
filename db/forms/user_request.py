from django import forms

from db.models import UserRequest


class UserRequestForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ('name', 'email', 'message', )
