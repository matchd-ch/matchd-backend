from wagtail.search.backends import get_search_backend

from db.models import Student, Company, JobPosting
from db.search.builders import StudentParamBuilder, CompanyParamBuilder
from db.search.resolvers import HitResolver


class Matching:
    search_backend = get_search_backend()

    def find_talents(self, branch_id=None, job_type_id=None, cultural_fits=None, soft_skills=None, skills=None,
                     languages=None, date_from=None, date_to=None):
        queryset = Student.get_indexed_objects()
        index = self.search_backend.get_index_for_model(queryset.model).name
        builder = StudentParamBuilder(queryset, index)
        if branch_id is not None:
            builder.set_branch(branch_id)
        if job_type_id is not None:
            builder.set_job_type(job_type_id)
        if cultural_fits is not None:
            builder.set_cultural_fits(cultural_fits)
        if soft_skills is not None:
            builder.set_soft_skills(soft_skills)
        if skills is not None:
            builder.set_skills(skills)
        if languages is not None:
            builder.set_languages(languages)
        if date_from is not None:
            if date_to is not None:
                builder.set_date_range(date_from, date_to)
            else:
                builder.set_date_from(date_from)
        print(builder.get_params())
        hits = self.search_backend.es.search(**builder.get_params())
        resolver = HitResolver(queryset, hits)
        return resolver.resolve()

    def find_companies(self, branch_id=None, cultural_fits=None, soft_skills=None):
        queryset = Company.get_indexed_objects()
        index = self.search_backend.get_index_for_model(queryset.model).name
        builder = CompanyParamBuilder(queryset, index)
        if branch_id is not None:
            builder.set_branch(branch_id)
        if cultural_fits is not None:
            builder.set_cultural_fits(cultural_fits)
        if soft_skills is not None:
            builder.set_soft_skills(soft_skills)
        hits = self.search_backend.es.search(**builder.get_params())
        resolver = HitResolver(queryset, hits)
        return resolver.resolve()

    def find_job_postings(self):
        queryset = JobPosting.get_indexed_objects()
        pass
