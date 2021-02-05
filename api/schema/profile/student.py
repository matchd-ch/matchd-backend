from datetime import datetime

import graphene
from django.core.exceptions import ValidationError
from graphql_auth.bases import Output
from django.utils.translation import gettext as _
from graphql_jwt.decorators import login_required

from api.helper import generic_error_dict, validation_error_to_dict
from api.validators import StudentProfileFormStepValidator
from db.forms.profile import StudentProfileFormStep6, StudentProfileFormStep1
from db.forms.profile.student import StudentProfileFormStep5
from db.helper import NicknameSuggestions
from db.models import UserType
from db.validators import NicknameValidator


class StudentProfileInputStep1(graphene.InputObjectType):
    first_name = graphene.String(description=_('First name'), required=True)
    last_name = graphene.String(description=_('Last name'), required=True)
    street = graphene.String(description=_('street'), required=True)
    zip = graphene.String(description=_('Zip'), required=True)
    city = graphene.String(description=_('City'), required=True)
    date_of_birth = graphene.String(description=_('Date of birth'), required=True)
    mobile = graphene.String(description=_('Date of birth'), required=True)


class StudentProfileStep1(Output, graphene.Mutation):

    class Arguments:
        step1 = StudentProfileInputStep1(description=_('Profile Input Step 1 is required.'))

    class Meta:
        description = _('Updates the profile of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        errors = {}
        user = info.context.user

        # validate user type
        if user.type not in UserType.valid_student_types():
            errors.update(generic_error_dict('type', _('You are not a student'), 'invalid_type'))
            return StudentProfileStep1(success=False, errors=errors)

        # validate step
        step_validator = StudentProfileFormStepValidator(1)
        try:
            step_validator.validate(user)
        except ValidationError as error:
            errors.update(validation_error_to_dict(error, 'profile_step'))
            return StudentProfileStep1(success=False, errors=errors)

        profile_data = data.get('step1', None)

        # convert date of birth
        try:
            date_of_birth = datetime.strptime(profile_data.get('date_of_birth'), "%d.%m.%Y").date()
            profile_data['date_of_birth'] = date_of_birth
        except ValueError as error:
            errors.update(generic_error_dict('date_of_birth', str(error), 'invalid'))

        # validate profile data
        profile = None
        profile_form = StudentProfileFormStep1(profile_data)
        profile_form.full_clean()
        if profile_form.is_valid():
            # update user / profile
            profile_data_for_update = profile_form.cleaned_data

            user.first_name = profile_data_for_update.get('first_name')
            user.last_name = profile_data_for_update.get('last_name')

            profile = user.student
            profile.street = profile_data_for_update.get('street')
            profile.zip = profile_data_for_update.get('zip')
            profile.city = profile_data_for_update.get('city')
            profile.date_of_birth = profile_data_for_update.get('date_of_birth')
            profile.mobile = profile_data_for_update.get('mobile')

            # update step only if the user has step 1
            if user.profile_step == 1:
                user.profile_step = 2
        else:
            errors.update(profile_form.errors.get_json_data())

        if errors:
            return StudentProfileStep1(success=False, errors=errors)

        # save user / profile
        user.save()
        profile.save()
        return StudentProfileStep1(success=True, errors=None)


class StudentProfileInputStep5(graphene.InputObjectType):
    nickname = graphene.String(description=_('Nickname'), required=True)


class StudentProfileStep5(Output, graphene.Mutation):

    nickname_suggestions = graphene.List(graphene.String)

    class Arguments:
        step5 = StudentProfileInputStep5(description=_('Profile Input Step 5 is required.'))

    class Meta:
        description = _('Updates the nickname of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        errors = {}
        user = info.context.user

        # validate user type
        if user.type not in UserType.valid_student_types():
            errors.update(generic_error_dict('type', _('You are not a student'), 'invalid_type'))
            return StudentProfileStep5(success=False, errors=errors)

        # validate step
        step_validator = StudentProfileFormStepValidator(5)
        try:
            step_validator.validate(user)
        except ValidationError as error:
            errors.update(validation_error_to_dict(error, 'profile_step'))
            return StudentProfileStep5(success=False, errors=errors)

        # validate profile data
        profile_data = data.get('step5', None)
        profile = None
        profile_form = StudentProfileFormStep5(profile_data)
        profile_form.full_clean()
        if profile_form.is_valid():
            # update user profile
            profile_data_for_update = profile_form.cleaned_data
            profile = user.student

            nickname = profile_data_for_update.get('nickname')
            try:
                nickname_validator = NicknameValidator()
                nickname_validator.validate(user, nickname)
            except ValidationError as error:
                errors.update(validation_error_to_dict(error, 'nickname'))
                nicknames = NicknameSuggestions()
                suggestions = nicknames.get_suggestions(user, nickname)
                return StudentProfileStep5(success=False, errors=errors, nickname_suggestions=suggestions)

            profile.nickname = profile_data_for_update.get('nickname')

            # update step only if the user has step 6
            if user.profile_step == 5:
                user.profile_step = 6
        else:
            errors.update(profile_form.errors.get_json_data())

        if errors:
            return StudentProfileStep5(success=False, errors=errors)

        # save user / profile
        user.save()
        profile.save()
        return StudentProfileStep5(success=True, errors=None)


class StudentProfileInputStep6(graphene.InputObjectType):
    state = graphene.String(description=_('State'), required=True)


class StudentProfileStep6(Output, graphene.Mutation):

    class Arguments:
        step6 = StudentProfileInputStep6(description=_('Profile Input Step 6 is required.'))

    class Meta:
        description = _('Updates the state of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        errors = {}
        user = info.context.user

        # validate user type
        if user.type not in UserType.valid_student_types():
            errors.update(generic_error_dict('type', _('You are not a student'), 'invalid_type'))
            return StudentProfileStep6(success=False, errors=errors)

        # validate step
        step_validator = StudentProfileFormStepValidator(6)
        try:
            step_validator.validate(user)
        except ValidationError as error:
            errors.update(validation_error_to_dict(error, 'profile_step'))
            return StudentProfileStep6(success=False, errors=errors)

        # validate profile data
        profile_data = data.get('step6', None)
        profile_form = StudentProfileFormStep6(profile_data)
        profile_form.full_clean()
        if profile_form.is_valid():
            # update user profile
            profile_data_for_update = profile_form.cleaned_data
            user.state = profile_data_for_update.get('state')

            # update step only if the user has step 6
            if user.profile_step == 6:
                user.profile_step = 7
        else:
            errors.update(profile_form.errors.get_json_data())

        if errors:
            return StudentProfileStep6(success=False, errors=errors)

        # save user / profile
        user.save()
        return StudentProfileStep6(success=True, errors=None)


class StudentProfileMutation(graphene.ObjectType):
    student_profile_step1 = StudentProfileStep1.Field()
    student_profile_step5 = StudentProfileStep5.Field()
    student_profile_step6 = StudentProfileStep6.Field()
