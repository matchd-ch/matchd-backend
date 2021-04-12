from django.conf import settings
from wagtail.search.backends import get_search_backend

from db.models import DateMode, JobPosting
from db.search.builders import JobPostingParamBuilder
from db.search.calculators import JobPostingScoreCalculator
from db.search.mapper import MatchMapper
from db.search.resolvers import HitResolver


# pylint: disable=R0913
class JobPostingMatching:
    search_backend = get_search_backend()

    def find_matches(self, user, job_type=None, branch=None, workload=None, zip_value=None, first=100, skip=0,
                     soft_boost=1, tech_boost=1):
        queryset = JobPosting.get_indexed_objects()
        index = self.search_backend.get_index_for_model(queryset.model).name
        if job_type is None:
            job_type = user.student.job_type
        if branch is None:
            branch = user.student.branch
        builder = JobPostingParamBuilder(queryset, index, first, skip)
        builder.set_branch(branch.id, settings.MATCHING_VALUE_BRANCH)
        builder.set_job_type(job_type.id, settings.MATCHING_VALUE_JOB_TYPE)
        builder.set_cultural_fits(user.student.cultural_fits.all(), soft_boost * settings.MATCHING_VALUE_CULTURAL_FITS)
        builder.set_soft_skills(user.student.soft_skills.all(), soft_boost * settings.MATCHING_VALUE_SOFT_SKILLS)
        builder.set_skills(user.student.skills.all(), tech_boost * settings.MATCHING_VALUE_SKILLS)
        if workload is not None:
            builder.set_workload(workload, settings.MATCHING_VALUE_WORKLOAD)
        if zip_value is not None:
            builder.set_zip(zip_value)
        date_mode = job_type.mode
        if date_mode == DateMode.DATE_RANGE:
            builder.set_date_range(user.student.job_from_date, user.student.job_to_date,
                                   settings.MATCHING_VALUE_DATE_OR_DATE_RANGE)
        else:
            builder.set_date_from(user.student.job_from_date, settings.MATCHING_VALUE_DATE_OR_DATE_RANGE)
        hits = self.search_backend.es.search(**builder.get_params())
        resolver = HitResolver(queryset, hits)
        hits = resolver.resolve()
        calculator = JobPostingScoreCalculator(user, hits, soft_boost, tech_boost)
        hits = calculator.annotate()
        return MatchMapper.map_job_postings(hits)
