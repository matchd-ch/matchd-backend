import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from api.helper import extract_ids, is_me_query, resolve_node_id, resolve_node_ids
from api.schema.branch import BranchInput
from api.schema.cultural_fit import CulturalFitInput
from api.schema.hobby import HobbyInput, Hobby
from api.schema.job_type import JobTypeInput
from api.schema.online_challenge import OnlineChallengeInput, OnlineChallenge
from api.schema.profile_state import ProfileState
from api.schema.soft_skill import SoftSkillInput
from api.schema.skill import SkillInput
from api.schema.user_language_relation.user_language_relation import UserLanguageRelationInput

from db.decorators import privacy_protection
from db.exceptions import FormException, NicknameException
from db.forms import process_student_base_data_form, process_student_character_form, process_student_employment_form, \
    process_student_specific_data_form, process_student_condition_form, process_student_abilities_form, \
    update_student_info
from db.models import Student as StudentModel, ProfileType, Match as MatchModel, ChallengeState
from db.helper.profile_calculator import get_relevant_student_profile_fields, \
    get_missing_relevant_student_profile_fields, calculate_student_profile_completion

# pylint: disable=W0221


class StudentInput(graphene.InputObjectType):
    id = graphene.String(required=True)


class RegisterStudentInput(graphene.InputObjectType):
    id = graphene.String(required=False)
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
    online_challenges = graphene.List(graphene.NonNull(OnlineChallenge))
    hobbies = graphene.List(graphene.NonNull(Hobby))
    date_of_birth = graphene.String()
    school_name = graphene.String()
    field_of_study = graphene.String()
    graduation = graphene.String()
    match_status = graphene.Field('api.schema.match.MatchStatus')
    challenges = graphene.NonNull(
        graphene.List(graphene.NonNull('api.schema.challenge.schema.Challenge')))
    is_matchable = graphene.NonNull(graphene.Boolean)
    profile_relevant_fields = graphene.List(graphene.NonNull(graphene.String))
    profile_missing_relevant_fields = graphene.List(graphene.NonNull(graphene.String))
    profile_completed_percentage = graphene.NonNull(graphene.Float)

    class Meta:
        model = StudentModel
        interfaces = (relay.Node, )
        fields = ('mobile', 'street', 'zip', 'city', 'date_of_birth', 'nickname', 'school_name',
                  'field_of_study', 'graduation', 'skills', 'hobbies', 'languages', 'distinction',
                  'online_challenges', 'state', 'soft_skills', 'cultural_fits', 'branch', 'slug',
                  'job_type', 'job_from_date', 'job_to_date', 'is_matchable')
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
    def resolve_online_challenges(self: StudentModel, info):
        return self.online_challenges.all()

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
            node_id = info.operation.selection_set.selections[0].arguments[1].value.value
            job_posting_id = resolve_node_id(node_id)
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
                node_id = info.variable_values.get('jobPostingId')
                job_posting_id = resolve_node_id(node_id)
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

    def resolve_challenges(self: StudentModel, info):
        if is_me_query(info):
            return self.challenges.all()
        return self.challenges.filter(state=ChallengeState.PUBLIC)

    def resolve_profile_relevant_fields(self: StudentModel, info):
        return get_relevant_student_profile_fields()

    def resolve_profile_missing_relevant_fields(self: StudentModel, info):
        return get_missing_relevant_student_profile_fields(self)

    def resolve_profile_completed_percentage(self: StudentModel, info):
        return calculate_student_profile_completion(self)


class StudentProfileBaseData(Output, relay.ClientIDMutation):

    class Input:
        first_name = graphene.String(description=_('First name'), required=False)
        last_name = graphene.String(description=_('Last name'), required=False)
        street = graphene.String(description=_('street'), required=False)
        zip = graphene.String(description=_('Zip'), required=False)
        city = graphene.String(description=_('City'), required=False)
        date_of_birth = graphene.String(description=_('Date of birth'), required=False)
        mobile = graphene.String(description=_('Date of birth'), required=False)

    class Meta:
        description = _('Updates the profile of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('input', None)
        try:
            process_student_base_data_form(user, form_data)
        except FormException as exception:
            return StudentProfileBaseData(success=False, errors=exception.errors)
        return StudentProfileBaseData(success=True, errors=None)


class StudentProfileEmployment(Output, relay.ClientIDMutation):

    class Input:
        job_type = graphene.Field(JobTypeInput, required=False)
        job_from_date = graphene.String(required=False)
        job_to_date = graphene.String(required=False)
        branch = graphene.Field(BranchInput, required=False)

    class Meta:
        description = _('Updates job option, date (start or range) and branch of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = resolve_node_ids(data.get('input', None))

        try:
            process_student_employment_form(user, form_data)
        except FormException as exception:
            return StudentProfileEmployment(success=False, errors=exception.errors)
        return StudentProfileEmployment(success=True, errors=None)


class StudentProfileCharacter(Output, relay.ClientIDMutation):

    class Input:
        soft_skills = graphene.List(SoftSkillInput, required=False)
        cultural_fits = graphene.List(CulturalFitInput, required=False)

    class Meta:
        description = _('Updates soft skills and cultural fits of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = resolve_node_ids(data.get('input', None))
        form_data['soft_skills'] = extract_ids(form_data.get('soft_skills', []), 'id')
        form_data['cultural_fits'] = extract_ids(form_data.get('cultural_fits', []), 'id')

        try:
            process_student_character_form(user, form_data)
        except FormException as exception:
            return StudentProfileCharacter(success=False, errors=exception.errors)
        return StudentProfileCharacter(success=True, errors=None)


class StudentProfileAbilities(Output, relay.ClientIDMutation):

    class Input:
        skills = graphene.List(SkillInput, description=_('Skills'), required=False)
        hobbies = graphene.List(HobbyInput, description=_('Hobbies'), required=False)
        online_challenges = graphene.List(OnlineChallengeInput,
                                          description=_('Online_Challenges'),
                                          required=False)
        languages = graphene.List(UserLanguageRelationInput,
                                  description=_('Languages'),
                                  required=False)
        distinction = graphene.String(description=_('Distinction'), required=False)

    class Meta:
        description = _('Updates the profile of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = resolve_node_ids(data.get('input', None), ['id', 'language', 'language_level'])
        form_data['skills'] = extract_ids(form_data.get('skills', []), 'id')

        try:
            process_student_abilities_form(user, form_data)
        except FormException as exception:
            return StudentProfileAbilities(success=False, errors=exception.errors)
        return StudentProfileAbilities(success=True, errors=None)


class StudentProfileSpecificData(Output, relay.ClientIDMutation):

    nickname_suggestions = graphene.List(graphene.String)

    class Input:
        nickname = graphene.String(description=_('Nickname'), required=False)

    class Meta:
        description = _('Updates the nickname of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('input', None)

        try:
            process_student_specific_data_form(user, form_data)
        except NicknameException as exception:
            return StudentProfileSpecificData(success=False,
                                              errors=exception.errors,
                                              nickname_suggestions=exception.suggestions)
        except FormException as exception:
            return StudentProfileSpecificData(success=False, errors=exception.errors)
        return StudentProfileSpecificData(success=True, errors=None)


class StudentProfileCondition(Output, relay.ClientIDMutation):

    class Input:
        state = graphene.String(description=_('State'), required=True)

    class Meta:
        description = _('Updates the state of a student')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('input', None)

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
                             job_posting_id=graphene.String(required=False))

    def resolve_student(self, info, slug, *args, **kwargs):
        user = info.context.user

        if user.type in ProfileType.valid_student_types() and user.student.slug != slug:
            raise PermissionDenied('You have not the permission to perform this action')

        student = get_object_or_404(StudentModel, slug=slug)

        return student


class UpdateStudentMutation(Output, relay.ClientIDMutation):
    student = graphene.Field(Student)

    class Input:
        is_matchable = graphene.Boolean(required=False)

    class Meta:
        description = _('Updates student information')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        student_data = data.get('input', None)

        try:
            updated_student = update_student_info(user, student_data)
        except FormException as exception:
            return UpdateStudentMutation(success=False, errors=exception.errors, student=None)
        return UpdateStudentMutation(success=True, errors=None, student=updated_student)


class StudentMutation(graphene.ObjectType):
    update_student = UpdateStudentMutation.Field()
