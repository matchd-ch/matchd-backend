import graphene
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from graphene import ObjectType
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from django.utils.translation import gettext as _
from graphql_jwt.decorators import login_required

from api.schema.branch import BranchInput
from api.schema.cultural_fit import CulturalFitInput
from api.schema.hobby import HobbyInput, Hobby
from api.schema.job_type import JobTypeInput
from api.schema.online_project import OnlineProjectInput, OnlineProject
from api.schema.profile_state import ProfileState
from api.schema.soft_skill import SoftSkillInput
from api.schema.skill import SkillInput
from api.schema.user_language_relation.user_language_relation import UserLanguageRelationInput
from db.decorators import privacy
from db.exceptions import FormException, NicknameException
from db.forms import process_student_form_step_1, process_student_form_step_2, \
    process_student_form_step_5, process_student_form_step_6, process_student_form_step_4
from db.forms.student_step_3 import process_student_form_step_3

from db.models import Student as StudentModel, ProfileType


class StudentInput(graphene.InputObjectType):
    id = graphene.ID(required=False)
    mobile = graphene.String(description=_('Mobile'), required=True)


class Student(DjangoObjectType):
    state = graphene.Field(graphene.NonNull(ProfileState))
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    zip = graphene.String()
    city = graphene.String()
    street = graphene.String()
    mobile = graphene.String()
    distinction = graphene.String()
    online_projects = graphene.List(graphene.NonNull(OnlineProject))
    hobbies = graphene.List(graphene.NonNull(Hobby))
    date_of_birth = graphene.String()
    school_name = graphene.String()
    field_of_study = graphene.String()
    graduation = graphene.String()

    class Meta:
        model = StudentModel
        fields = ('id', 'mobile', 'street', 'zip', 'city', 'date_of_birth', 'nickname', 'school_name', 'field_of_study',
                  'graduation', 'skills', 'hobbies', 'languages', 'distinction', 'online_projects', 'state',
                  'profile_step', 'soft_skills', 'cultural_fits', 'branch', 'slug', 'job_type', 'job_type',
                  'branch', 'job_from_date', 'job_to_date')
        convert_choices_to_enum = False

    @privacy
    def resolve_first_name(self: StudentModel, info):
        return self.user.first_name

    @privacy
    def resolve_last_name(self: StudentModel, info):
        return self.user.last_name

    @privacy
    def resolve_email(self: StudentModel, info):
        return self.user.email

    @privacy
    def resolve_zip(self: StudentModel, info):
        return self.zip

    @privacy
    def resolve_city(self: StudentModel, info):
        return self.city

    @privacy
    def resolve_street(self: StudentModel, info):
        return self.street

    @privacy
    def resolve_mobile(self: StudentModel, info):
        return self.mobile

    @privacy
    def resolve_distinction(self: StudentModel, info):
        return self.distinction

    @privacy
    def resolve_online_projects(self: StudentModel, info):
        return self.online_projects

    @privacy
    def resolve_hobbies(self: StudentModel, info):
        return self.hobbies

    @privacy
    def resolve_date_of_birth(self: StudentModel, info):
        return self.date_of_birth

    @privacy
    def resolve_school_name(self: StudentModel, info):
        return self.school_name

    @privacy
    def resolve_field_of_study(self: StudentModel, info):
        return self.field_of_study

    @privacy
    def resolve_graduation(self: StudentModel, info):
        return self.graduation


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
    job_type = graphene.Field(JobTypeInput, required=True)
    job_from_date = graphene.String(required=False)
    job_to_date = graphene.String(required=False)
    branch = graphene.Field(BranchInput, required=False)


class StudentProfileStep2(Output, graphene.Mutation):

    class Arguments:
        step2 = StudentProfileInputStep2(description=_('Profile Input Step 2 is required.'), required=True)

    class Meta:
        description = _('Updates job option, date (start or range) and branch of a student')

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
    soft_skills = graphene.List(SoftSkillInput, required=False)
    cultural_fits = graphene.List(CulturalFitInput, required=False)


class StudentProfileStep3(Output, graphene.Mutation):

    class Arguments:
        step3 = StudentProfileInputStep3(description=_('Profile Input Step 3 is required.'), required=True)

    class Meta:
        description = _('Updates soft skills and cultural fits of a student')

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
    skills = graphene.List(SkillInput, description=_('Skills'), required=False)
    hobbies = graphene.List(HobbyInput, description=_('Hobbies'), required=False)
    online_projects = graphene.List(OnlineProjectInput, description=_('Online_Projects'), required=False)
    languages = graphene.List(UserLanguageRelationInput, description=_('Languages'), required=True)
    distinction = graphene.String(description=_('Distinction'), required=False)


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


class StudentQuery(ObjectType):
    student = graphene.Field(Student, slug=graphene.String())

    def resolve_student(self, info, slug):
        user = info.context.user

        if user.type not in (ProfileType.COMPANY, ProfileType.UNIVERSITY):
            if user.type in ProfileType.valid_student_types() and user.student.slug != slug:
                raise PermissionDenied('You have not the permission to perform this action')

        student = get_object_or_404(StudentModel, slug=slug)
        if student.state == ProfileState.INCOMPLETE:
            raise Http404('Student not found')
        return student
