from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.http import Http404
from wagtail.search.backends import get_search_backend

from db.models import Student, DateMode, ProfileType, JobPosting, JobPostingLanguageRelation, JobPostingState
from db.search.builders import StudentParamBuilder
from db.search.calculators.student import StudentScoreCalculator
from db.search.mapper import MatchMapper
from db.search.resolvers import HitResolver


# pylint: disable=R0913
class StudentMatching:
    search_backend = get_search_backend()

    def __init__(self, user, data, first, skip, tech_boost, soft_boost):
        self.user = user
        self.data = data
        self.job_posting = None
        self.first = first
        self.skip = skip
        self.tech_boost = tech_boost
        self.soft_boost = soft_boost

    def _validate_input(self):
        if self.user.type not in ProfileType.valid_company_types():
            raise PermissionDenied('You do not have the permission to perform this action')
        job_posting_id = self.data.get('job_posting').get('id')
        try:
            self.job_posting = JobPosting.objects.prefetch_related(
                Prefetch(
                    'languages',
                    queryset=JobPostingLanguageRelation.objects.filter(job_posting_id=job_posting_id).select_related(
                        'language', 'language_level')
                )
            ).select_related('company').get(pk=job_posting_id)
        except JobPosting.DoesNotExist:
            raise Http404('Job posting does not exist')

        if self.job_posting.state != JobPostingState.PUBLIC:
            raise PermissionDenied('You do not have the permission to perform this action')

        job_posting_company = self.job_posting.company
        if self.user.company != job_posting_company:
            raise PermissionDenied('You do not have the permission to perform this action')

    def find_matches(self):
        self._validate_input()
        queryset = Student.get_indexed_objects()
        index = self.search_backend.get_index_for_model(queryset.model).name

        builder = StudentParamBuilder(queryset, index, self.first, self.skip)
        builder.set_branch(self.job_posting.branch_id, settings.MATCHING_VALUE_BRANCH)
        builder.set_job_type(self.job_posting.job_type_id, settings.MATCHING_VALUE_JOB_TYPE)
        builder.set_cultural_fits(self.job_posting.company.cultural_fits.all(), self.soft_boost *
                                  settings.MATCHING_VALUE_CULTURAL_FITS)
        builder.set_soft_skills(self.job_posting.company.soft_skills.all(),
                                self.soft_boost * settings.MATCHING_VALUE_SOFT_SKILLS)
        builder.set_skills(self.job_posting.skills.all(), self.tech_boost * settings.MATCHING_VALUE_SKILLS)
        if self.job_posting.job_from_date is not None:
            date_mode = self.job_posting.job_type.mode
            if date_mode == DateMode.DATE_RANGE:
                builder.set_date_range(self.job_posting.job_from_date, self.job_posting.job_to_date,
                                       settings.MATCHING_VALUE_DATE_OR_DATE_RANGE)
            else:
                builder.set_date_from(self.job_posting.job_from_date, settings.MATCHING_VALUE_DATE_OR_DATE_RANGE)
        hits = self.search_backend.es.search(**builder.get_params())
        resolver = HitResolver(queryset, hits)
        hits = resolver.resolve()
        calculator = StudentScoreCalculator(self.job_posting, hits, self.soft_boost, self.tech_boost)
        hits = calculator.annotate()
        return MatchMapper.map_students(hits)
