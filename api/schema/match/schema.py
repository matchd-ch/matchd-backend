import graphene
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required
from graphene import ObjectType, InputObjectType, relay

from django.utils.translation import gettext as _

from api.schema.branch import BranchInput
from api.schema.keyword.schema import Keyword
from api.schema.profile_type import ProfileType
from api.schema.project_posting.schema import ProjectPostingInput
from api.schema.student import StudentInput
from api.schema.zip_city import ZipCityInput
from api.schema.job_posting import JobPostingInput
from api.schema.job_type import JobTypeInput

from db.context.match.matching_factory import MatchingFactory
from db.exceptions import FormException
from db.forms import process_job_posting_match, process_student_match, process_project_posting_match
from db.models import MatchType as MatchTypeModel, Match as MatchModel

MatchType = graphene.Enum.from_enum(MatchTypeModel)


class MatchHints(ObjectType):
    has_requested_match = graphene.NonNull(graphene.Boolean)
    has_confirmed_match = graphene.NonNull(graphene.Boolean)


class MatchStatus(ObjectType):
    confirmed = graphene.NonNull(graphene.Boolean)
    initiator = graphene.Field(graphene.NonNull(ProfileType))


class JobPostingMatchInfo(DjangoObjectType):
    student = graphene.NonNull('api.schema.student.schema.Student')
    job_posting = graphene.NonNull('api.schema.job_posting.schema.JobPosting')

    class Meta:
        model = MatchModel
        interfaces = (relay.Node, )
        fields = (
            'student',
            'job_posting',
        )


class ProjectPostingMatchInfo(DjangoObjectType):
    student = graphene.Field('api.schema.student.schema.Student')
    company = graphene.Field('api.schema.company.schema.Company')
    project_posting = graphene.NonNull('api.schema.project_posting.schema.ProjectPosting')

    class Meta:
        model = MatchModel
        interfaces = (relay.Node, )
        fields = (
            'student',
            'project_posting',
            'company',
        )


class Match(ObjectType):
    id = graphene.ID()
    slug = graphene.NonNull(graphene.String)
    name = graphene.NonNull(graphene.String)
    type = graphene.NonNull(MatchType)
    avatar = graphene.String()
    score = graphene.NonNull(graphene.Float)
    raw_score = graphene.NonNull(graphene.Float)
    title = graphene.String()
    match_status = graphene.Field(MatchStatus)
    description = graphene.String()
    keywords = graphene.List(graphene.NonNull(Keyword))


class StudentMatchingInput(InputObjectType):
    job_posting = graphene.Field(JobPostingInput, required=True)


class JobPostingMatchingInput(InputObjectType):
    branch = graphene.Field(BranchInput, required=False)
    job_type = graphene.Field(JobTypeInput, required=False)
    workload = graphene.Int(required=False)
    zip = graphene.Field(ZipCityInput, required=False)


class ProjectPostingMatchingInput(InputObjectType):
    project_posting = graphene.Field(ProjectPostingInput, required=True)


class MatchQuery(ObjectType):
    matches = graphene.List(Match,
                            first=graphene.Int(required=False, default_value=100),
                            skip=graphene.Int(required=False, default_value=0),
                            tech_boost=graphene.Int(required=False, default_value=3),
                            soft_boost=graphene.Int(required=False, default_value=3),
                            job_posting_matching=graphene.Argument(JobPostingMatchingInput,
                                                                   required=False),
                            student_matching=graphene.Argument(StudentMatchingInput,
                                                               required=False),
                            project_posting_matching=graphene.Argument(ProjectPostingMatchingInput,
                                                                       required=False))

    @login_required
    def resolve_matches(self, info, **kwargs):
        user = info.context.user

        return MatchingFactory().get_matching_context(user, **kwargs).find_matches()


class MatchStudentInput(graphene.InputObjectType):
    student = graphene.Field(StudentInput, required=True)
    job_posting = graphene.Field(JobPostingInput, required=True)


class MatchStudent(Output, graphene.Mutation):

    confirmed = graphene.NonNull(graphene.Boolean)

    class Arguments:
        match = MatchStudentInput(description=_('MatchInput'), required=True)

    class Meta:
        description = _('Initiate or confirm Matching')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        try:
            match_obj = process_student_match(user, data.get('match'))
        except FormException as exception:
            return MatchStudent(success=False, errors=exception.errors, confirmed=False)
        return MatchStudent(success=True, errors=None, confirmed=match_obj.complete)


class MatchJobPostingInput(graphene.InputObjectType):
    job_posting = graphene.Field(JobPostingInput, required=True)


class MatchJobPosting(Output, graphene.Mutation):

    confirmed = graphene.NonNull(graphene.Boolean)

    class Arguments:
        match = MatchJobPostingInput(description=_('MatchInput'), required=True)

    class Meta:
        description = _('Initiate or confirm Matching')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        try:
            match_obj = process_job_posting_match(user, data.get('match'))
        except FormException as exception:
            return MatchJobPosting(success=False, errors=exception.errors, confirmed=False)
        return MatchJobPosting(success=True, errors=None, confirmed=match_obj.complete)


class MatchProjectPostingInput(graphene.InputObjectType):
    project_posting = graphene.Field(ProjectPostingInput, required=True)


class MatchProjectPosting(Output, graphene.Mutation):

    confirmed = graphene.NonNull(graphene.Boolean)

    class Arguments:
        match = MatchProjectPostingInput(description=_('MatchInput'), required=True)

    class Meta:
        description = _('Initiate or confirm Matching')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        try:
            match_obj = process_project_posting_match(user, data.get('match'))
        except FormException as exception:
            return MatchProjectPosting(success=False, errors=exception.errors, confirmed=False)
        return MatchProjectPosting(success=True, errors=None, confirmed=match_obj.complete)


class MatchMutation(graphene.ObjectType):
    match_student = MatchStudent.Field()
    match_job_posting = MatchJobPosting.Field()
    match_project_posting = MatchProjectPosting.Field()
