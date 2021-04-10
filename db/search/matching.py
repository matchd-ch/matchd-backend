from wagtail.search.backends import get_search_backend

from db.models import Student, Company, DateMode
from db.search.builders import StudentParamBuilder, CompanyParamBuilder
from db.search.resolvers import HitResolver


# pylint: disable=R0913
class Matching:
    search_backend = get_search_backend()

    def find_talents_by_job_posting(self, job_posting, first=100, skip=0, soft_boost=1, tech_boost=1):
        queryset = Student.get_indexed_objects().prefetch_related('user')
        index = self.search_backend.get_index_for_model(queryset.model).name
        maximum_score = self.calculate_maximum_job_posting_score(job_posting, soft_boost, tech_boost)

        builder = StudentParamBuilder(queryset, index, first, skip)
        builder.set_branch(job_posting.branch_id, 10)
        builder.set_job_type(job_posting.job_type_id, 10)
        builder.set_cultural_fits(job_posting.company.cultural_fits.all(), soft_boost)
        builder.set_soft_skills(job_posting.company.soft_skills.all(), soft_boost)
        builder.set_skills(job_posting.skills.all(), tech_boost)
        languages = job_posting.languages.all()
        if languages is not None:
            builder.set_languages(languages)
        if job_posting.job_from_date is not None:
            date_mode = job_posting.job_type.mode
            if date_mode == DateMode.DATE_RANGE:
                builder.set_date_range(job_posting.job_from_date, job_posting.job_to_date)
            else:
                builder.set_date_from(job_posting.job_from_date)

        hits = self.search_backend.es.search(**builder.get_params())
        resolver = HitResolver(queryset, hits, maximum_score)
        return resolver.resolve()

    def find_companies(self, branch_id=None, cultural_fits=None, soft_skills=None, job_type_id=None, soft_boost=1,
                       tech_boost=1, first=100, skip=0):
        queryset = Company.get_indexed_objects()
        index = self.search_backend.get_index_for_model(queryset.model).name
        builder = CompanyParamBuilder(queryset, index, first, skip)
        if branch_id is not None:
            builder.set_branch(branch_id, 10)
        if job_type_id is not None:
            builder.set_job_type(job_type_id, 10)
        if cultural_fits is not None:
            builder.set_cultural_fits(cultural_fits, soft_boost)
        if soft_skills is not None:
            builder.set_soft_skills(soft_skills, soft_boost)
        hits = self.search_backend.es.search(**builder.get_params())
        resolver = HitResolver(queryset, hits, 1000)
        return resolver.resolve()

    def find_job_postings(self):
        # queryset = JobPosting.get_indexed_objects()
        pass

    def calculate_maximum_job_posting_score(self, job_posting, soft_boost, tech_boost):
        # Calculate the maximum score possible
        # branch id, job type id
        maximum_score = 20
        maximum_score += (len(job_posting.company.cultural_fits.all()) * soft_boost)
        maximum_score += (len(job_posting.company.soft_skills.all()) * soft_boost)
        maximum_score += (len(job_posting.skills.all()) * tech_boost)
        # matching on language level is disabled for now, see db.search.builders.student (set_languages)
        # we do not add the score for the language, to get better matching scores
        # maximum_score += (len(job_posting.languages.all()) * 2)
        if job_posting.job_type.mode == DateMode.DATE_RANGE:
            maximum_score += 6  # max score for date or date range match
        else:
            maximum_score += 3  # max score for date or date range match
        return maximum_score
