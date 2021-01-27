from django import forms

from db.models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('uid', 'name', 'zip', 'city')
