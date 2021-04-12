from django.conf import settings
from wagtail.search.backends import get_search_backend

from db.models import Student, DateMode
from db.search.builders import StudentParamBuilder
from db.search.calculators.student import StudentScoreCalculator
from db.search.mapper import MatchMapper
from db.search.resolvers import HitResolver


# pylint: disable=R0913
class StudentMatching:
    search_backend = get_search_backend()

    def find_matches(self, job_posting, first=100, skip=0, soft_boost=1, tech_boost=1):
        queryset = Student.get_indexed_objects().prefetch_related('user', 'languages', 'languages__language_level')
        index = self.search_backend.get_index_for_model(queryset.model).name

        builder = StudentParamBuilder(queryset, index, first, skip)
        builder.set_branch(job_posting.branch_id, settings.MATCHING_VALUE_BRANCH)
        builder.set_job_type(job_posting.job_type_id, settings.MATCHING_VALUE_JOB_TYPE)
        builder.set_cultural_fits(job_posting.company.cultural_fits.all(), soft_boost *
                                  settings.MATCHING_VALUE_CULTURAL_FITS)
        builder.set_soft_skills(job_posting.company.soft_skills.all(), soft_boost * settings.MATCHING_VALUE_SOFT_SKILLS)
        builder.set_skills(job_posting.skills.all(), tech_boost * settings.MATCHING_VALUE_SKILLS)
        if job_posting.job_from_date is not None:
            date_mode = job_posting.job_type.mode
            if date_mode == DateMode.DATE_RANGE:
                builder.set_date_range(job_posting.job_from_date, job_posting.job_to_date)
            else:
                builder.set_date_from(job_posting.job_from_date)
        hits = self.search_backend.es.search(**builder.get_params())
        resolver = HitResolver(queryset, hits)
        hits = resolver.resolve()
        calculator = StudentScoreCalculator(job_posting, hits, soft_boost, tech_boost)
        hits = calculator.annotate()
        return MatchMapper.map_students(hits)
