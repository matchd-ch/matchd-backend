from django import forms

from db.exceptions import FormException
from db.helper.forms import validate_form_data, validate_company_user_type
from db.models import ProfileType, Branch, Benefit


class UniversityProfileRelationsForm(forms.Form):
    branches = forms.ModelMultipleChoiceField(queryset=Branch.objects.all(), required=False)
    benefits = forms.ModelMultipleChoiceField(queryset=Benefit.objects.all(), required=False)

    services = forms.CharField(max_length=3000, required=False)
    link_education = forms.URLField(max_length=2048, required=False)
    link_challenges = forms.URLField(max_length=2048, required=False)
    link_thesis = forms.URLField(max_length=2048, required=False)


def process_university_relations_form(user, data):
    # validate user type, data
    validate_company_user_type(user, ProfileType.UNIVERSITY)
    validate_form_data(data)
    errors = {}
    company = user.company

    benefits_to_save = None
    branches_to_save = None

    # validate profile data
    form = UniversityProfileRelationsForm(data)
    form.full_clean()
    if form.is_valid():
        # update user / profile
        cleaned_data = form.cleaned_data
        company.services = cleaned_data.get('services')
        company.link_education = cleaned_data.get('link_education')
        company.link_challenges = cleaned_data.get('link_challenges')
        company.link_thesis = cleaned_data.get('link_thesis')
        branches_to_save = cleaned_data.get('branches')
        benefits_to_save = cleaned_data.get('benefits')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # save user / profile
    user.save()
    company.save()
    company.benefits.set(benefits_to_save)
    company.branches.set(branches_to_save)
