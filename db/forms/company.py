from django import forms
from django.forms.models import model_to_dict

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
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, _ in self.fields.items():
            self.fields[key].required = False


def update_company_info(company, data):
    errors = {}

    form_data = model_to_dict(company)
    form_data.update(data)

    form = CompanyCompleteForm(form_data, instance=company)

    form.full_clean()

    if form.is_valid():
        company = form.save()
    else:
        errors.update(form.errors.get_json_data())
        raise FormException(errors=errors)

    return company
