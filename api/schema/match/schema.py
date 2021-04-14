import graphene
from graphql_jwt.decorators import login_required
from graphene import ObjectType, InputObjectType

from api.schema.branch import BranchInput
from api.schema.zip_city import ZipCityInput
from api.schema.job_posting import JobPostingInput
from api.schema.job_type import JobTypeInput
from db.models import MatchType as MatchTypeModel
from db.search.matching import JobPostingMatching, StudentMatching

MatchType = graphene.Enum.from_enum(MatchTypeModel)


class Match(ObjectType):
    id = graphene.ID()
    slug = graphene.NonNull(graphene.String)
    name = graphene.NonNull(graphene.String)
    type = graphene.NonNull(MatchType)
    avatar = graphene.String()
    score = graphene.NonNull(graphene.Float)
    raw_score = graphene.NonNull(graphene.Float)
    job_posting_title = graphene.String()


class StudentMatchingInput(InputObjectType):
    job_posting = graphene.Field(JobPostingInput, required=True)


class JobPostingMatchingInput(InputObjectType):
    branch = graphene.Field(BranchInput, required=False)
    job_type = graphene.Field(JobTypeInput, required=False)
    workload = graphene.Int(required=False)
    zip = graphene.Field(ZipCityInput, required=False)


class MatchQuery(ObjectType):
    matches = graphene.List(
        Match,
        first=graphene.Int(required=False, default_value=100),
        skip=graphene.Int(required=False, default_value=0),
        tech_boost=graphene.Int(required=False, default_value=3),
        soft_boost=graphene.Int(required=False, default_value=3),
        job_posting_matching=graphene.Argument(JobPostingMatchingInput, required=False),
        student_matching=graphene.Argument(StudentMatchingInput, required=False)
    )

    @login_required
    def resolve_matches(self, info, **kwargs):
        user = info.context.user
        first = kwargs.get('first')
        skip = kwargs.get('skip')

        # normalize boost
        soft_boost = max(min(kwargs.get('soft_boost', 1), 5), 1)
        tech_boost = max(min(kwargs.get('tech_boost', 1), 5), 1)

        job_posting_matching = kwargs.get('job_posting_matching', None)
        if job_posting_matching is not None:
            matching = JobPostingMatching(user, job_posting_matching, first, skip, tech_boost, soft_boost)
            return matching.find_matches()

        student_matching = kwargs.get('student_matching', None)
        if student_matching is not None:
            matching = StudentMatching(user, student_matching, first, skip, tech_boost, soft_boost)
            return matching.find_matches()
        return []
