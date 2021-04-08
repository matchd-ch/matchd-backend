from wagtail.search.backends import get_search_backend

from db.models import Student, Company, JobPosting
from db.search.builders import StudentParamBuilder, CompanyParamBuilder
from db.search.resolvers import HitResolver


class Matching:
    search_backend = get_search_backend()

    def find_talents(self, branch_id=None, job_type_id=None, cultural_fits=None, soft_skills=None, skills=None,
                     languages=None, date_from=None, date_to=None, soft_boost=1, tech_boost=1, first=100, skip=0):
        queryset = Student.get_indexed_objects().prefetch_related('user')
        index = self.search_backend.get_index_for_model(queryset.model).name
        builder = StudentParamBuilder(queryset, index, first, skip)
        if branch_id is not None:
            builder.set_branch(branch_id, 10)
        if job_type_id is not None:
            builder.set_job_type(job_type_id, 10)
        if cultural_fits is not None:
            builder.set_cultural_fits(cultural_fits, soft_boost)
        if soft_skills is not None:
            builder.set_soft_skills(soft_skills, soft_boost)
        if skills is not None:
            builder.set_skills(skills, tech_boost)
        if languages is not None:
            builder.set_languages(languages)
        if date_from is not None:
            if date_to is not None:
                builder.set_date_range(date_from, date_to)
            else:
                builder.set_date_from(date_from)
        hits = self.search_backend.es.search(**builder.get_params())
        resolver = HitResolver(queryset, hits)
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
        resolver = HitResolver(queryset, hits)
        return resolver.resolve()

    def find_job_postings(self):
        queryset = JobPosting.get_indexed_objects()
        pass
