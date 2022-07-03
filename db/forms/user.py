from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings
from django.forms.models import model_to_dict

from db.exceptions import FormException

# pylint: disable=W5104


class UserForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = '__all__'
        exclude = settings.GRAPHQL_AUTH.get('USER_NODE_EXCLUDE_FIELDS')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, _ in self.fields.items():
            self.fields[key].required = False


def update_user_info(user, data):
    errors = {}

    form_data = model_to_dict(user)
    form_data.update(data)

    user_form = UserForm(form_data, instance=user)
    user_form.full_clean()

    if user_form.is_valid():
        user = user_form.save()

        if 'email' in user_form.changed_data:
            user.status.verified = False
            user.status.save(update_fields=["verified"])
    else:
        errors.update(user_form.errors.get_json_data())
        raise FormException(errors=errors)

    return user
