from wagtail.search.backends import get_search_backend

from db.models import Student, Company, JobPosting
from db.search.builders import StudentParamBuilder, CompanyParamBuilder
from db.search.resolvers import HitResolver


class Matching:
    search_backend = get_search_backend()

    def find_talents(self, branch_id=None):
        queryset = Student.get_indexed_objects()
        index = self.search_backend.get_index_for_model(queryset.model).name
        builder = StudentParamBuilder(queryset, index)
        if branch_id is not None:
            builder.set_branch(branch_id)
        hits = self.search_backend.es.search(**builder.get_params())
        resolver = HitResolver(queryset, hits)
        return resolver.resolve()

    def find_companies(self, branch_id=None):
        queryset = Company.get_indexed_objects()
        index = self.search_backend.get_index_for_model(queryset.model).name
        builder = CompanyParamBuilder(queryset, index)
        if branch_id is not None:
            builder.set_branch(branch_id)
        hits = self.search_backend.es.search(**builder.get_params())
        resolver = HitResolver(queryset, hits)
        return resolver.resolve()

    def find_job_postings(self):
        queryset = JobPosting.get_indexed_objects()
        pass
