import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from api.helper import is_me_query
from api.schema.branch import BranchInput
from api.schema.cultural_fit import CulturalFitInput
from api.schema.hobby import HobbyInput, Hobby
from api.schema.job_type import JobTypeInput
from api.schema.online_project import OnlineProjectInput, OnlineProject
from api.schema.profile_state import ProfileState
from api.schema.soft_skill import SoftSkillInput
from api.schema.skill import SkillInput
from api.schema.user_language_relation.user_language_relation import UserLanguageRelationInput

from db.decorators import privacy_protection
from db.exceptions import FormException, NicknameException
from db.forms import process_student_base_data_form, process_student_character_form, process_student_employment_form, \
    process_student_specific_data_form, process_student_condition_form, process_student_abilities_form
from db.models import Student as StudentModel, ProfileType, Match as MatchModel, ProjectPostingState


class StudentInput(graphene.InputObjectType):
    id = graphene.ID(required=True)


class RegisterStudentInput(graphene.InputObjectType):
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
    match_status = graphene.Field('api.schema.match.MatchStatus')
    project_postings = graphene.NonNull(
        graphene.List(graphene.NonNull('api.schema.project_posting.schema.ProjectPosting')))

    class Meta:
        model = StudentModel
        interfaces = (relay.Node, )
        fields = ('mobile', 'street', 'zip', 'city', 'date_of_birth', 'nickname', 'school_name',
                  'field_of_study', 'graduation', 'skills', 'hobbies', 'languages', 'distinction',
                  'online_projects', 'state', 'profile_step', 'soft_skills', 'cultural_fits',
                  'branch', 'slug', 'job_type', 'job_from_date', 'job_to_date')
        convert_choices_to_enum = False

    @privacy_protection()
    def resolve_first_name(self: StudentModel, info):
        return self.user.first_name

    @privacy_protection()
    def resolve_last_name(self: StudentModel, info):
        return self.user.last_name

    @privacy_protection(match_only=True)
    def resolve_email(self: StudentModel, info):
        return self.user.email

    @privacy_protection(match_only=True)
    def resolve_zip(self: StudentModel, info):
        return self.zip

    @privacy_protection(match_only=True)
    def resolve_city(self: StudentModel, info):
        return self.city

    @privacy_protection(match_only=True)
    def resolve_street(self: StudentModel, info):
        return self.street

    @privacy_protection(match_only=True)
    def resolve_mobile(self: StudentModel, info):
        return self.mobile

    @privacy_protection()
    def resolve_distinction(self: StudentModel, info):
        return self.distinction

    @privacy_protection()
    def resolve_online_projects(self: StudentModel, info):
        return self.online_projects.all()

    @privacy_protection()
    def resolve_hobbies(self: StudentModel, info):
        return self.hobbies.all()

    @privacy_protection()
    def resolve_date_of_birth(self: StudentModel, info):
        return self.date_of_birth

    @privacy_protection()
    def resolve_school_name(self: StudentModel, info):
        return self.school_name

    @privacy_protection()
    def resolve_field_of_study(self: StudentModel, info):
        return self.field_of_study

    @privacy_protection()
    def resolve_graduation(self: StudentModel, info):
        return self.graduation

    # noinspection PyBroadException
    def resolve_match_status(self: StudentModel, info):
        # try to retrieve job posting id parameter from operation
        #
        # query example:
        # query
        # {
        #     student(slug: "{student-slug}", jobPostingId: {id}) {
        #     .....
        #     }
        # }
        try:
            job_posting_id = info.operation.selection_set.selections[0].arguments[1].value.value
        except Exception:
            job_posting_id = None

        # fallback if request was sent with variables
        #
        # query example:
        # query($slug: String!, $jobPostingId: ID!) {
        #     student(slug: $slug, jobPostingId: $jobPostingId) {
        #     ....
        #     }
        # }
        # with variables
        # {
        #     "slug": "{student-slug}",
        #     "jobPostingId": {id}
        # }
        if job_posting_id is None:
            try:
                job_posting_id = info.variable_values.get('jobPostingId')
            except Exception:
                job_posting_id = None

        # if the parameter is missing, no match status will be returned
        if job_posting_id is None:
            return None

        user = info.context.user
        status = None
        if user.type in ProfileType.valid_company_types():
            try:
                status = MatchModel.objects.get(student=self, job_posting__id=job_posting_id)
            except MatchModel.DoesNotExist:
                pass

        if status is not None:
            return {'confirmed': status.complete, 'initiator': status.initiator}
        return None

    def resolve_project_postings(self: StudentModel, info):
        if is_me_query(info):
            return self.project_postings.all()
        return self.project_postings.filter(state=ProjectPostingState.PUBLIC)


class StudentProfileInputBaseData(graphene.InputObjectType):
    first_name = graphene.String(description=_('First name'), required=True)
    last_name = graphene.String(description=_('Last name'), required=True)
    street = graphene.String(description=_('street'))
    zip = graphene.String(description=_('Zip'))
    city = graphene.String(description=_('City'))
    date_of_birth = graphene.String(description=_('Date of birth'), required=True)
    mobile = graphene.String(description=_('Date of birth'))


class StudentProfileBaseData(Output, graphene.Mutation):

    class Arguments:
        base_data = StudentProfileInputBaseData(
            description=_('Profile Input Base Data is required.'), required=True)

    class Meta:
        description = _('Updates the profile of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('base_data', None)
        try:
            process_student_base_data_form(user, form_data)
        except FormException as exception:
            return StudentProfileBaseData(success=False, errors=exception.errors)
        return StudentProfileBaseData(success=True, errors=None)


class StudentProfileInputEmployment(graphene.InputObjectType):
    job_type = graphene.Field(JobTypeInput, required=True)
    job_from_date = graphene.String(required=False)
    job_to_date = graphene.String(required=False)
    branch = graphene.Field(BranchInput, required=False)


class StudentProfileEmployment(Output, graphene.Mutation):

    class Arguments:
        employment = StudentProfileInputEmployment(
            description=_('Profile Input Employment is required.'), required=True)

    class Meta:
        description = _('Updates job option, date (start or range) and branch of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('employment', None)
        try:
            process_student_employment_form(user, form_data)
        except FormException as exception:
            return StudentProfileEmployment(success=False, errors=exception.errors)
        return StudentProfileEmployment(success=True, errors=None)


class StudentProfileInputCharacter(graphene.InputObjectType):
    soft_skills = graphene.List(SoftSkillInput, required=False)
    cultural_fits = graphene.List(CulturalFitInput, required=False)


class StudentProfileCharacter(Output, graphene.Mutation):

    class Arguments:
        character = StudentProfileInputCharacter(
            description=_('Profile Input Character is required.'), required=True)

    class Meta:
        description = _('Updates soft skills and cultural fits of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('character', None)
        try:
            process_student_character_form(user, form_data)
        except FormException as exception:
            return StudentProfileCharacter(success=False, errors=exception.errors)
        return StudentProfileCharacter(success=True, errors=None)


class StudentProfileInputAbilities(graphene.InputObjectType):
    skills = graphene.List(SkillInput, description=_('Skills'), required=False)
    hobbies = graphene.List(HobbyInput, description=_('Hobbies'), required=False)
    online_projects = graphene.List(OnlineProjectInput,
                                    description=_('Online_Projects'),
                                    required=False)
    languages = graphene.List(UserLanguageRelationInput, description=_('Languages'), required=True)
    distinction = graphene.String(description=_('Distinction'), required=False)


class StudentProfileAbilities(Output, graphene.Mutation):

    class Arguments:
        abilities = StudentProfileInputAbilities(
            description=_('Profile Input Abilities is required.'))

    class Meta:
        description = _('Updates the profile of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('abilities', None)
        try:
            process_student_abilities_form(user, form_data)
        except FormException as exception:
            return StudentProfileAbilities(success=False, errors=exception.errors)
        return StudentProfileAbilities(success=True, errors=None)


class StudentProfileInputSpecificData(graphene.InputObjectType):
    nickname = graphene.String(description=_('Nickname'), required=True)


class StudentProfileSpecificData(Output, graphene.Mutation):

    nickname_suggestions = graphene.List(graphene.String)

    class Arguments:
        specific_data = StudentProfileInputSpecificData(
            description=_('Profile Input Specific Data is required.'), required=True)

    class Meta:
        description = _('Updates the nickname of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('specific_data', None)
        try:
            process_student_specific_data_form(user, form_data)
        except NicknameException as exception:
            return StudentProfileSpecificData(success=False,
                                              errors=exception.errors,
                                              nickname_suggestions=exception.suggestions)
        except FormException as exception:
            return StudentProfileSpecificData(success=False, errors=exception.errors)
        return StudentProfileSpecificData(success=True, errors=None)


class StudentProfileInputCondition(graphene.InputObjectType):
    state = graphene.String(description=_('State'), required=True)


class StudentProfileCondition(Output, graphene.Mutation):

    class Arguments:
        condition = StudentProfileInputCondition(
            description=_('Profile Input Condition is required.'), required=True)

    class Meta:
        description = _('Updates the state of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('condition', None)
        try:
            process_student_condition_form(user, form_data)
        except FormException as exception:
            return StudentProfileCondition(success=False, errors=exception.errors)
        return StudentProfileCondition(success=True, errors=None)


class StudentProfileMutation(ObjectType):
    student_profile_base_data = StudentProfileBaseData.Field()
    student_profile_employment = StudentProfileEmployment.Field()
    student_profile_character = StudentProfileCharacter.Field()
    student_profile_abilities = StudentProfileAbilities.Field()
    student_profile_specific_data = StudentProfileSpecificData.Field()
    student_profile_condition = StudentProfileCondition.Field()


class StudentQuery(ObjectType):
    student = graphene.Field(Student,
                             slug=graphene.String(),
                             job_posting_id=graphene.ID(required=False))

    def resolve_student(self, info, slug, *args, **kwargs):
        user = info.context.user

        if user.type in ProfileType.valid_student_types() and user.student.slug != slug:
            raise PermissionDenied('You have not the permission to perform this action')

        student = get_object_or_404(StudentModel, slug=slug)
        if student.state == ProfileState.INCOMPLETE:
            raise Http404('Student not found')
        return student
