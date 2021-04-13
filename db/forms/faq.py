from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from graphql_jwt.exceptions import PermissionDenied

from db.exceptions import FormException
from db.helper import validate_form_data
from db.helper.forms import validate_company_user_type, convert_object_to_id, generic_error_dict
from db.models import ProfileType, FAQCategory, FAQ


class AddFAQForm(forms.Form):
    category = forms.ModelChoiceField(queryset=FAQCategory.objects.all(), required=True)
    title = forms.CharField(max_length=250, required=True)
    question = forms.CharField(max_length=1000, required=True)
    answer = forms.CharField(max_length=1000, required=True)

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data['category'] = convert_object_to_id(data.get('category', None))
        super().__init__(data=data, **kwargs)


def process_add_faq(user, data):
    # validate user type and data
    validate_company_user_type(user, ProfileType.COMPANY)
    validate_form_data(data)
    errors = {}
    company = user.company

    # validate profile data
    form = AddFAQForm(data)
    form.full_clean()
    faq_to_save = FAQ()
    if form.is_valid():
        cleaned_data = form.cleaned_data

        # required parameters
        faq_to_save.category = cleaned_data.get('category')
        faq_to_save.title = cleaned_data.get('title')
        faq_to_save.question = cleaned_data.get('question')
        faq_to_save.answer = cleaned_data.get('answer')
        faq_to_save.company = company

    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # save FAQ
    faq_to_save.save()


class UpdateFAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['category', 'title', 'question', 'answer']

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelForm and graphene_django
        data['category'] = convert_object_to_id(data.get('category', None))
        super().__init__(data=data, **kwargs)


def process_update_faq(user, data):
    # validate user type and data
    validate_company_user_type(user, ProfileType.COMPANY)
    validate_form_data(data)
    errors = {}
    company = user.company

    faq_to_save = get_object_or_404(FAQ, pk=data.get('faq_id'))
    # check if company matches
    if not faq_to_save.company == company:
        raise PermissionDenied('You do not have permission to perform this action')

    # validate profile data
    form = UpdateFAQForm(data, instance=faq_to_save)
    form.full_clean()

    if form.is_valid():
        form.save()

    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)


def process_delete_faq(user, data):
    # validate user type and data
    validate_company_user_type(user, ProfileType.COMPANY)
    validate_form_data(data)
    company = user.company

    faq_to_remove = get_object_or_404(FAQ, pk=data.get('faq_id'))
    # check if company matches
    if faq_to_remove.company == company:
        faq_to_remove.delete()
    else:
        raise PermissionDenied('You do not have permission to perform this action')
