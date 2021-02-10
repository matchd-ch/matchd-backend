import graphene
from django.core.exceptions import ValidationError
from graphql_auth.bases import Output
from django.utils.translation import gettext as _
from graphql_jwt.decorators import login_required

from db.helper import generic_error_dict, validation_error_to_dict, validate_user_type_step_and_data
from api.schema.job_option import JobOptionInputType
from api.schema.job_position import JobPositionInputType
from db.helper.forms import convert_date
from db.exceptions import FormException
from db.forms.profile import StudentProfileFormStep6, StudentProfileFormStep1, StudentProfileFormStep5, \
    StudentProfileFormStep2, StudentProfileFormStep3, StudentProfileFormStep3DateRange, StudentProfileFormStep3Date
from db.helper import NicknameSuggestions
from db.models import JobOption, JobOptionMode
from db.validators import NicknameValidator


class StudentProfileInputStep1(graphene.InputObjectType):
    first_name = graphene.String(description=_('First name'), required=True)
    last_name = graphene.String(description=_('Last name'), required=True)
    street = graphene.String(description=_('street'))
    zip = graphene.String(description=_('Zip'))
    city = graphene.String(description=_('City'))
    date_of_birth = graphene.String(description=_('Date of birth'), required=True)
    mobile = graphene.String(description=_('Date of birth'))


class StudentProfileStep1(Output, graphene.Mutation):

    class Arguments:
        step1 = StudentProfileInputStep1(description=_('Profile Input Step 1 is required.'), required=True)

    class Meta:
        description = _('Updates the profile of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        errors = {}
        user = info.context.user

        # profile data
        profile_data = data.get('step1', None)

        # validate user type, step and data
        try:
            validate_user_type_step_and_data(user, profile_data, 1)
        except FormException as exception:
            return StudentProfileStep2(success=False, errors=exception.errors)

        # convert date of birth to date
        try:
            profile_data = convert_date(profile_data, 'date_of_birth')
        except FormException as exception:
            errors.update(exception.errors)

        # validate profile data
        profile = None
        profile_form = StudentProfileFormStep1(profile_data)
        profile_form.full_clean()
        if profile_form.is_valid():
            # update user / profile
            profile = user.student
            profile_data_for_update = profile_form.cleaned_data

            # required parameters
            user.first_name = profile_data_for_update.get('first_name')
            user.last_name = profile_data_for_update.get('last_name')
            profile.date_of_birth = profile_data_for_update.get('date_of_birth')

            # optional parameters
            profile.street = profile_data_for_update.get('street')
            profile.zip = profile_data_for_update.get('zip')
            profile.city = profile_data_for_update.get('city')
            profile.mobile = profile_data_for_update.get('mobile')
        else:
            errors.update(profile_form.errors.get_json_data())

        if errors:
            return StudentProfileStep1(success=False, errors=errors)

        # update step only if the user has step 1
        if user.profile_step == 1:
            user.profile_step = 2

        # save user / profile
        user.save()
        profile.save()
        return StudentProfileStep1(success=True, errors=None)


class StudentProfileInputStep2(graphene.InputObjectType):
    school_name = graphene.String(description=_('School name'))
    field_of_study = graphene.String(description=_('Field of study'))
    graduation = graphene.String(description=_('Graduation'))


class StudentProfileStep2(Output, graphene.Mutation):

    class Arguments:
        step2 = StudentProfileInputStep2(description=_('Profile Input Step 2 is required.'), required=True)

    class Meta:
        description = _('Updates school name, field of study and graduation')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        errors = {}
        user = info.context.user

        # profile data
        profile_data = data.get('step2', None)

        # validate user type, step and data
        try:
            validate_user_type_step_and_data(user, profile_data, 2)
        except FormException as exception:
            return StudentProfileStep2(success=False, errors=exception.errors)

        # convert graduation to date
        try:
            profile_data = convert_date(profile_data, 'graduation', '%m.%Y', False)
        except FormException as exception:
            errors.update(exception.errors)

        profile = None
        profile_form = StudentProfileFormStep2(profile_data)
        profile_form.full_clean()
        if profile_form.is_valid():
            # update user / profile
            profile = user.student
            profile_data_for_update = profile_form.cleaned_data

            # optional parameters
            profile.field_of_study = profile_data_for_update.get('field_of_study')
            profile.school_name = profile_data_for_update.get('school_name')
            profile.graduation = profile_data_for_update.get('graduation')
        else:
            errors.update(profile_form.errors.get_json_data())

        if errors:
            return StudentProfileStep2(success=False, errors=errors)

        # update step only if the user has step 2
        if user.profile_step == 2:
            user.profile_step = 3

        # save user / profile
        user.save()
        profile.save()

        return StudentProfileStep2(success=True, errors=None)


class StudentProfileInputStep3(graphene.InputObjectType):
    job_option = graphene.Field(JobOptionInputType, required=True)
    job_from_date = graphene.String(required=False)
    job_to_date = graphene.String(required=False)
    job_position = graphene.Field(JobPositionInputType, required=False)


class StudentProfileStep3(Output, graphene.Mutation):

    class Arguments:
        step3 = StudentProfileInputStep3(description=_('Profile Input Step 3 is required.'), required=True)

    class Meta:
        description = _('Updates job option, date (start or range) and job position of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        errors = {}
        user = info.context.user

        # profile data
        profile_data = data.get('step3', None)

        # validate user type, step and data
        try:
            validate_user_type_step_and_data(user, profile_data, 3)
        except FormException as exception:
            return StudentProfileStep3(success=False, errors=exception.errors)

        profile = None
        profile_form = StudentProfileFormStep3(profile_data)
        profile_form.full_clean()

        if profile_form.is_valid():
            # update user profile
            profile_data_for_update = profile_form.cleaned_data
            profile = user.student

            # required parameters
            profile.job_option = profile_data_for_update.get('job_option')

            # optional parameters
            profile.job_position = profile_data_for_update.get('job_position')
        else:
            errors.update(profile_form.errors.get_json_data())

        job_option = JobOption.objects.get(pk=profile.job_option.id)

        if 'job_from_date' in profile_data and profile_data.get('job_from_date', None) is not None:

            # convert fromDate / toDate
            try:
                profile_data = convert_date(profile_data, 'job_from_date', '%m.%Y')
            except FormException as exception:
                errors.update(exception.errors)

            # we need different forms for different option types
            #
            # JobOptionTypeChoices.DATE_RANGE:
            # we need two valid dates and a valid date range (both dates are required)
            #
            # JobOptionTypeChoices.DATE_FROM:
            # we need one valid date and need to reset the second date (only one date is required)

            if job_option.mode == JobOptionMode.DATE_RANGE:
                try:
                    profile_data = convert_date(profile_data, 'job_to_date', '%m.%Y')
                except FormException as exception:
                    errors.update(exception.errors)

                date_form = StudentProfileFormStep3DateRange(profile_data)
                date_form.full_clean()
                if date_form.is_valid():
                    # update profile
                    profile_data_for_update = date_form.cleaned_data

                    # validate date range
                    from_date = profile_data_for_update.get('job_from_date')
                    to_date = profile_data_for_update.get('job_to_date')
                    if from_date >= to_date:
                        errors.update(generic_error_dict('job_to_date', _('Date must be after other date'),
                                                         'invalid_range'))
                    else:
                        profile.job_from_date = from_date
                        profile.job_to_date = to_date
                else:
                    errors.update(date_form.errors.get_json_data())
            else:
                date_form = StudentProfileFormStep3Date(profile_data)
                date_form.full_clean()
                if date_form.is_valid():
                    # update profile
                    profile_data_for_update = date_form.cleaned_data
                    profile.job_from_date = profile_data_for_update.get('job_from_date')

                    # reset to date
                    profile.job_to_date = None
                else:
                    errors.update(date_form.errors.get_json_data())

        if errors:
            return StudentProfileStep3(success=False, errors=errors)

        # update step only if the user has step 2
        if user.profile_step == 3:
            user.profile_step = 4

        # save user / profile
        user.save()
        profile.save()

        return StudentProfileStep3(success=True, errors=None)


class StudentProfileInputStep5(graphene.InputObjectType):
    nickname = graphene.String(description=_('Nickname'), required=True)


class StudentProfileStep5(Output, graphene.Mutation):

    nickname_suggestions = graphene.List(graphene.String)

    class Arguments:
        step5 = StudentProfileInputStep5(description=_('Profile Input Step 5 is required.'), required=True)

    class Meta:
        description = _('Updates the nickname of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        errors = {}
        user = info.context.user

        # profile data
        profile_data = data.get('step5', None)

        # validate user type, step and data
        try:
            validate_user_type_step_and_data(user, profile_data, 5)
        except FormException as exception:
            return StudentProfileStep2(success=False, errors=exception.errors)

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
        else:
            errors.update(profile_form.errors.get_json_data())

        if errors:
            return StudentProfileStep5(success=False, errors=errors)

        # update step only if the user has step 6
        if user.profile_step == 5:
            user.profile_step = 6

        # save user / profile
        user.save()
        profile.save()

        return StudentProfileStep5(success=True, errors=None)


class StudentProfileInputStep6(graphene.InputObjectType):
    state = graphene.String(description=_('State'), required=True)


class StudentProfileStep6(Output, graphene.Mutation):

    class Arguments:
        step6 = StudentProfileInputStep6(description=_('Profile Input Step 6 is required.'), required=True)

    class Meta:
        description = _('Updates the state of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        errors = {}
        user = info.context.user

        # profile data
        profile_data = data.get('step6', None)

        # validate user type, step and data
        try:
            validate_user_type_step_and_data(user, profile_data, 6)
        except FormException as exception:
            return StudentProfileStep2(success=False, errors=exception.errors)

        profile_form = StudentProfileFormStep6(profile_data)
        profile_form.full_clean()
        if profile_form.is_valid():
            # update user profile
            profile_data_for_update = profile_form.cleaned_data
            user.state = profile_data_for_update.get('state')
        else:
            errors.update(profile_form.errors.get_json_data())

        if errors:
            return StudentProfileStep6(success=False, errors=errors)

        # update step only if the user has step 6
        if user.profile_step == 6:
            user.profile_step = 7

        # save user
        user.save()

        return StudentProfileStep6(success=True, errors=None)


class StudentProfileMutation(graphene.ObjectType):
    student_profile_step1 = StudentProfileStep1.Field()
    student_profile_step2 = StudentProfileStep2.Field()
    student_profile_step3 = StudentProfileStep3.Field()
    student_profile_step5 = StudentProfileStep5.Field()
    student_profile_step6 = StudentProfileStep6.Field()
