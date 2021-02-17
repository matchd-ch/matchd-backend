import graphene
from graphql_auth.bases import Output
from django.utils.translation import gettext as _
from graphql_jwt.decorators import login_required

from api.schema.hobby import HobbyInputType
from api.schema.job_option import JobOptionInputType
from api.schema.job_position import JobPositionInputType
from api.schema.online_project import OnlineProjectInputType
from api.schema.skill import SkillInputType
from api.schema.user_language_relation.user_language_relation import UserLanguageRelationInputType
from db.exceptions import FormException, NicknameException
from db.forms import process_student_form_step_1, process_student_form_step_2, process_student_form_step_3, \
    process_student_form_step_5, process_student_form_step_6, process_student_form_step_4


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
        user = info.context.user
        form_data = data.get('step1', None)
        try:
            process_student_form_step_1(user, form_data)
        except FormException as exception:
            return StudentProfileStep1(success=False, errors=exception.errors)
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
        user = info.context.user
        form_data = data.get('step2', None)
        try:
            process_student_form_step_2(user, form_data)
        except FormException as exception:
            return StudentProfileStep2(success=False, errors=exception.errors)
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
        user = info.context.user
        form_data = data.get('step3', None)
        try:
            process_student_form_step_3(user, form_data)
        except FormException as exception:
            return StudentProfileStep3(success=False, errors=exception.errors)
        return StudentProfileStep3(success=True, errors=None)


class StudentProfileInputStep4(graphene.InputObjectType):
    skills = graphene.List(SkillInputType, description=_('Skills'), required=False)
    hobbies = graphene.List(HobbyInputType, description=_('Hobbies'), required=False)
    online_projects = graphene.List(OnlineProjectInputType, description=_('Online_Projects'), required=False)
    languages = graphene.List(UserLanguageRelationInputType, description=_('Languages'), required=True)
    distinction = graphene.List(description=_('Distinction'), required=False)


class StudentProfileStep4(Output, graphene.Mutation):
    class Arguments:
        step4 = StudentProfileInputStep4(description=_('Profile Input Step 4 is required.'))

    class Meta:
        description = _('Updates the profile of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('step4', None)
        try:
            process_student_form_step_4(user, form_data)
        except FormException as exception:
            return StudentProfileStep4(success=False, errors=exception.errors)
        return StudentProfileStep4(success=True, errors=None)


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
        user = info.context.user
        form_data = data.get('step5', None)
        try:
            process_student_form_step_5(user, form_data)
        except NicknameException as exception:
            return StudentProfileStep5(success=False, errors=exception.errors,
                                       nickname_suggestions=exception.suggestions)
        except FormException as exception:
            return StudentProfileStep5(success=False, errors=exception.errors)
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
        user = info.context.user
        form_data = data.get('step6', None)
        try:
            process_student_form_step_6(user, form_data)
        except FormException as exception:
            return StudentProfileStep6(success=False, errors=exception.errors)
        return StudentProfileStep6(success=True, errors=None)


class StudentProfileMutation(graphene.ObjectType):
    student_profile_step1 = StudentProfileStep1.Field()
    student_profile_step2 = StudentProfileStep2.Field()
    student_profile_step3 = StudentProfileStep3.Field()
    student_profile_step4 = StudentProfileStep4.Field()
    student_profile_step5 = StudentProfileStep5.Field()
    student_profile_step6 = StudentProfileStep6.Field()
