from datetime import datetime

import graphene
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.http import Http404
from graphql_jwt.decorators import login_required
from graphene import ObjectType, InputObjectType

from api.mapper import MatchMapper
from api.schema.job_posting import JobPostingInput
from api.schema.profile_type import ProfileType
from db.models import JobPosting as JobPostingModel, DateMode, JobPostingLanguageRelation
from db.search import Matching


class Match(ObjectType):
    name = graphene.NonNull(graphene.String)
    avatar = graphene.String()
    type = graphene.Field(ProfileType)
    slug = graphene.NonNull(graphene.String)
    score = graphene.NonNull(graphene.Float)


class JobPostingMatchingInput(InputObjectType):
    job_posting = graphene.Field(JobPostingInput, required=True)
    tech_boost = graphene.Int(required=True)
    soft_boost = graphene.Int(required=True)


class MatchQuery(ObjectType):
    matches = graphene.List(
        Match,
        first=graphene.Int(required=False, default_value=100),
        skip=graphene.Int(required=False, default_value=0),
        job_posting_matching=graphene.Argument(JobPostingMatchingInput, required=False)
    )

    @login_required
    def resolve_matches(self, info, **kwargs):
        user = info.context.user
        first = kwargs.get('first')
        skip = kwargs.get('skip')
        job_posting_matching = kwargs.get('job_posting_matching', None)
        if job_posting_matching is not None:
            return MatchQuery.job_posting_matching(user, job_posting_matching, first, skip)
        return []

    @classmethod
    def job_posting_matching(cls, user, data, first, skip):
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
        job_posting_company = job_posting.company
        if user.company != job_posting_company:
            raise PermissionDenied('You do not have permission to search with this job posting')
        soft_boost = max(min(data.get('soft_boost', 1), 5), 1)
        tech_boost = max(min(data.get('tech_boost', 1), 5), 1)
        matching = Matching()
        date_mode = job_posting.job_type.mode
        params = {
            'first': first,
            'skip': skip,
            'soft_boost': soft_boost,
            'tech_boost': tech_boost,
            'branch_id': job_posting.branch_id,
            'job_type_id': job_posting.job_type_id,
            'cultural_fits': job_posting_company.cultural_fits.all(),
            'soft_skills': job_posting_company.soft_skills.all(),
            'skills': job_posting.skills.all(),
            'languages': job_posting.languages.all(),
            'date_from': job_posting.job_from_date
        }
        if date_mode == DateMode.DATE_RANGE:
            params['date_to'] = job_posting.job_to_date

        matches = matching.find_talents(**params)
        matches = MatchMapper.map_students(matches)
        return matches

    @classmethod
    def student_matching(cls, user, data, first, skip):
        # matching = Matching()
        # matches = matching.find_companies(branch_id=branch, cultural_fits=user.student.cultural_fits.all(),
        #                                   soft_skills=user.student.soft_skills.all(), first=first, skip=skip)
        # matches = MatchMapper.map_companies(matches)
        # return matches
        return []