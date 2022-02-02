from django import forms

from db.models import OnlineProject


class OnlineProjectForm(forms.ModelForm):

    class Meta:
        model = OnlineProject
        fields = (
            'id',
            'url',
            'student',
        )
