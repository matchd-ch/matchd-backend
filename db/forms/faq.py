from django import forms

from db.exceptions import FormException
from db.helper import validate_form_data
from db.helper.forms import validate_company_user_type, convert_object_to_id
from db.models import ProfileType, FAQCategory, FAQ


class FAQForm(forms.Form):
    category = forms.ModelChoiceField(queryset=FAQCategory.objects.all(), required=True)
    title = forms.CharField(max_length=250, required=True)
    question = forms.CharField(max_length=1000, required=True)
    answer = forms.CharField(max_length=1000, required=True)

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data['category'] = convert_object_to_id(data.get('category', None))
        super().__init__(data=data, **kwargs)


def process_faq(user, data):
    print(FAQCategory.objects.all())
    # validate user type, step and data
    validate_company_user_type(user, ProfileType.COMPANY)
    validate_form_data(data)
    errors = {}
    company = user.company

    # validate profile data
    form = FAQForm(data)
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
