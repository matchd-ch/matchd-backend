from django import forms

from db.models import Hobby


class HobbyForm(forms.ModelForm):

    class Meta:
        model = Hobby
        fields = (
            'id',
            'name',
            'student',
        )
