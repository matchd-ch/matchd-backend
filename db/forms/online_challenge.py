from django import forms

from db.models import OnlineChallenge


class OnlineChallengeForm(forms.ModelForm):

    class Meta:
        model = OnlineChallenge
        fields = (
            'id',
            'url',
            'student',
        )
