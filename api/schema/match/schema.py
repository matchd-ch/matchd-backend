import graphene
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404
from graphql_jwt.decorators import login_required
from graphene import ObjectType, InputObjectType

from api.schema.branch import BranchInput
from api.schema.zip_city import ZipCityInput
from api.schema.job_posting import JobPostingInput
from api.schema.job_type import JobTypeInput
from db.models import JobPosting as JobPostingModel, JobPostingLanguageRelation, JobType as JobTypeModel,  \
    ProfileType as ProfileTypeModel, JobPostingState, MatchType as MatchTypeModel, Branch as BranchModel
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


class JobPostingMatchingInput(InputObjectType):
    job_posting = graphene.Field(JobPostingInput, required=True)


class StudentMatchingInput(InputObjectType):
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
            return MatchQuery.job_posting_matching(user, job_posting_matching, first, skip, tech_boost, soft_boost)

        student_matching = kwargs.get('student_matching', None)
        if student_matching is not None:
            return MatchQuery.student_matching(user, student_matching, first, skip, tech_boost, soft_boost)
        return []

    # pylint: disable=R0913
    # pylint: disable=W0707
    @classmethod
    def job_posting_matching(cls, user, data, first, skip, tech_boost, soft_boost):
        if user.type not in ProfileTypeModel.valid_company_types():
            raise PermissionDenied('You do not have the permission to perform this action')

        job_posting_id = data.get('job_posting').get('id')
        try:
            job_posting = JobPostingModel.objects.prefetch_related(
                Prefetch(
                    'languages',
                    queryset=JobPostingLanguageRelation.objects.filter(job_posting_id=job_posting_id).select_related(
                        'language', 'language_level')
                )
            ).select_related('company').get(pk=job_posting_id)
        except JobPostingModel.DoesNotExist:
            raise Http404('Job posting does not exist')

        if job_posting.state != JobPostingState.PUBLIC:
            raise PermissionDenied('You do not have the permission to perform this action')

        job_posting_company = job_posting.company
        if user.company != job_posting_company:
            raise PermissionDenied('You do not have the permission to perform this action')

        matching = JobPostingMatching()
        return matching.find_matches(job_posting, first, skip, soft_boost, tech_boost)

    # pylint: disable=R0913
    @classmethod
    def student_matching(cls, user, data, first, skip, tech_boost, soft_boost):
        if user.type not in ProfileTypeModel.valid_student_types():
            raise PermissionDenied('You do not have the permission to perform this action')

        job_type_id = data.get('job_type', None)
        if job_type_id is not None:
            job_type_id = job_type_id.get('id')

        job_type = None
        if job_type_id is not None:
            job_type = get_object_or_404(JobTypeModel, pk=job_type_id)

        branch_id = data.get('branch', None)
        if branch_id is not None:
            branch_id = branch_id.get('id')

        branch = None
        if branch_id is not None:
            branch = get_object_or_404(BranchModel, pk=branch_id)

        workload = data.get('workload', None)
        zip_value = data.get('zip', None)
        if zip_value is not None:
            zip_value = zip_value.get('zip', None)

        matching = StudentMatching()
        return matching.find_matches(user, job_type, branch, workload, zip_value, first, skip, soft_boost, tech_boost)
