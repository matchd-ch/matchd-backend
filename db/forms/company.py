from django import forms

from db.exceptions import FormException
from db.models import Company


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('uid', 'name', 'zip', 'city', 'type', 'slug')


class UniversityForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('name', 'zip', 'city', 'type', 'slug')


class CompanyCompleteForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('name', 'state')


def update_company_info(company, data):
    errors = {}

    form = CompanyCompleteForm(data, instance=company)

    form.full_clean()

    if form.is_valid():
        company = form.save()
    else:
        errors.update(form.errors.get_json_data())
        raise FormException(errors=errors)

    return company
