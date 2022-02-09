from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from wagtail.search.backends import get_search_backend

from db.context.match.matching import Matching
from db.models import DateMode, JobPosting, ProfileType, JobType, Branch
from db.search.builders import JobPostingParamBuilder
from db.search.calculators import JobPostingScoreCalculator
from db.search.mapper import JobPostingMatchMapper
from db.search.resolvers import HitResolver


# pylint: disable=R0913
# pylint: disable=R0902
class JobPostingMatching(Matching):
    search_backend = get_search_backend()

    def __init__(self, user, **kwargs):
        super().__init__(user, **kwargs)

        self.job_type = None
        self.branch = None
        self.workload = 100
        self.zip_value = None

    def _validate_input(self):
        if self._user.type not in ProfileType.valid_student_types():
            raise PermissionDenied('You do not have the permission to perform this action')

        job_type_id = self.data.get('job_type', None)
        if job_type_id is not None:
            job_type_id = job_type_id.get('id')
        if job_type_id is not None:
            self.job_type = get_object_or_404(JobType, pk=job_type_id)
        if self.job_type is None:
            self.job_type = self._user.student.job_type
        branch_id = self.data.get('branch', None)
        if branch_id is not None:
            branch_id = branch_id.get('id')
        if branch_id is not None:
            self.branch = get_object_or_404(Branch, pk=branch_id)
        if self.branch is None:
            self.branch = self._user.student.branch

        workload = self.data.get('workload', None)
        if workload is not None:
            self.workload = workload

        zip_value = self.data.get('zip', None)
        if zip_value is not None:
            self.zip_value = zip_value.get('zip', None)

    def find_matches(self):
        self._validate_input()
        queryset = JobPosting.get_indexed_objects()
        index = self.search_backend.get_index_for_model(queryset.model).name

        builder = JobPostingParamBuilder(queryset, index, self.first, self.skip)
        if self.branch is not None:
            builder.set_branch(self.branch.id, settings.MATCHING_VALUE_BRANCH)
        builder.set_job_type(self.job_type.id, settings.MATCHING_VALUE_JOB_TYPE)
        builder.set_cultural_fits(self._user.student.cultural_fits.all(),
                                  self.soft_boost * settings.MATCHING_VALUE_CULTURAL_FITS)
        builder.set_soft_skills(self._user.student.soft_skills.all(),
                                self.soft_boost * settings.MATCHING_VALUE_SOFT_SKILLS)
        builder.set_skills(self._user.student.skills.all(),
                           self.tech_boost * settings.MATCHING_VALUE_SKILLS)
        builder.set_workload(self.workload, settings.MATCHING_VALUE_WORKLOAD)
        if self.zip_value is not None:
            builder.set_zip(self.zip_value)
        date_mode = self.job_type.mode
        if date_mode == DateMode.DATE_RANGE and self._user.student.job_to_date is not None:
            builder.set_date_range(self._user.student.job_from_date, self._user.student.job_to_date,
                                   settings.MATCHING_VALUE_DATE_OR_DATE_RANGE)
        else:
            builder.set_date_from(self._user.student.job_from_date,
                                  settings.MATCHING_VALUE_DATE_OR_DATE_RANGE)
        hits = self.search_backend.es.search(**builder.get_params())
        resolver = HitResolver(queryset, hits)
        hits = resolver.resolve()
        calculator = JobPostingScoreCalculator(self._user, hits, self.soft_boost, self.tech_boost)
        hits = calculator.annotate()
        mapper = JobPostingMatchMapper(hits, self.user)
        return mapper.get_matches()
