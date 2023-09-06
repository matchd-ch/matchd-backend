import graphene
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required
from graphene import ObjectType, InputObjectType, relay

from django.utils.translation import gettext as _

from api.helper import resolve_node_ids
from api.schema.branch import BranchInput
from api.schema.keyword.schema import Keyword
from api.schema.profile_type import ProfileType
from api.schema.challenge.schema import ChallengeInput
from api.schema.student import StudentInput
from api.schema.job_posting import JobPostingInput
from api.schema.job_type import JobTypeInput

from db.context.match.matching_factory import MatchingFactory
from db.exceptions import FormException
from db.forms import process_job_posting_match, process_student_match, process_challenge_match
from db.models import MatchType as MatchTypeModel, Match as MatchModel

# pylint: disable=W0221

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


class ChallengeMatchInfo(DjangoObjectType):
    student = graphene.Field('api.schema.student.schema.Student')
    company = graphene.Field('api.schema.company.schema.Company')
    challenge = graphene.NonNull('api.schema.challenge.schema.Challenge')

    class Meta:
        model = MatchModel
        interfaces = (relay.Node, )
        fields = (
            'student',
            'challenge',
            'company',
        )


class Match(ObjectType):
    id = graphene.String()
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
    zip = graphene.String(required=False)


class ChallengeMatchingInput(InputObjectType):
    challenge = graphene.Field(ChallengeInput, required=True)


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
                            challenge_matching=graphene.Argument(ChallengeMatchingInput,
                                                                 required=False))

    @login_required
    def resolve_matches(self, info, **kwargs):
        user = info.context.user
        data = resolve_node_ids(kwargs)

        return MatchingFactory().get_matching_context(user, **data).find_matches()


class MatchStudent(Output, relay.ClientIDMutation):

    confirmed = graphene.NonNull(graphene.Boolean)

    class Input:
        student = graphene.Field(StudentInput, required=True)
        job_posting = graphene.Field(JobPostingInput, required=True)

    class Meta:
        description = _('Initiate or confirm Matching')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        input_data = resolve_node_ids(data.get('input'))

        try:
            match_obj = process_student_match(user, input_data, info.context)
        except FormException as exception:
            return MatchStudent(success=False, errors=exception.errors, confirmed=False)
        return MatchStudent(success=True, errors=None, confirmed=match_obj.complete)


class MatchJobPosting(Output, relay.ClientIDMutation):

    confirmed = graphene.NonNull(graphene.Boolean)

    class Input:
        job_posting = graphene.Field(JobPostingInput, required=True)

    class Meta:
        description = _('Initiate or confirm Matching')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        input_data = resolve_node_ids(data.get('input'))

        try:
            match_obj = process_job_posting_match(user, input_data, info.context)
        except FormException as exception:
            return MatchJobPosting(success=False, errors=exception.errors, confirmed=False)
        return MatchJobPosting(success=True, errors=None, confirmed=match_obj.complete)


class MatchChallenge(Output, relay.ClientIDMutation):

    confirmed = graphene.NonNull(graphene.Boolean)

    class Input:
        challenge = graphene.Field(ChallengeInput, required=True)

    class Meta:
        description = _('Initiate or confirm Matching')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        input_data = resolve_node_ids(data.get('input'))

        try:
            match_obj = process_challenge_match(user, input_data, info.context)
        except FormException as exception:
            return MatchChallenge(success=False, errors=exception.errors, confirmed=False)
        return MatchChallenge(success=True, errors=None, confirmed=match_obj.complete)


class MatchMutation(graphene.ObjectType):
    match_student = MatchStudent.Field()
    match_job_posting = MatchJobPosting.Field()
    match_challenge = MatchChallenge.Field()
