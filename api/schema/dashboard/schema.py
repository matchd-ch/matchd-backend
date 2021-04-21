import graphene
from graphene import ObjectType

from api.schema.job_posting.schema import JobPosting


class Dashboard(ObjectType):
    job_postings = graphene.List(graphene.NonNull(JobPosting))


class DashboardQuery(ObjectType):
    dashboard = graphene.Field(Dashboard)

    def resolve_dashboard(self, info, **kwargs):
        return {
            'job_postings': []
        }
