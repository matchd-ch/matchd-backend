import graphene
from graphene import ObjectType
from graphql_jwt.decorators import login_required

from django.core.exceptions import PermissionDenied

from api.schema.job_posting.schema import JobPosting
from api.schema.project_posting.schema import ProjectPosting
from api.schema.match import JobPostingMatchInfo, ProjectPostingMatchInfo

from db.context.dashboard.dashboard_data_factory import DashboardDataFactory
from db.models import ProfileType


class Dashboard(ObjectType):
    job_postings = graphene.List(graphene.NonNull(JobPosting))
    project_postings = graphene.List(graphene.NonNull(ProjectPosting))
    latest_job_postings = graphene.List(graphene.NonNull(JobPosting))
    latest_project_postings = graphene.List(graphene.NonNull(ProjectPosting))
    requested_matches = graphene.List(graphene.NonNull(JobPostingMatchInfo))
    unconfirmed_matches = graphene.List(graphene.NonNull(JobPostingMatchInfo))
    confirmed_matches = graphene.List(graphene.NonNull(JobPostingMatchInfo))
    project_matches = graphene.List(graphene.NonNull(ProjectPostingMatchInfo))


class DashboardQuery(ObjectType):
    dashboard = graphene.Field(Dashboard)

    @login_required
    def resolve_dashboard(self, info, **kwargs):
        user = info.context.user

        if user.type not in ProfileType.valid_company_types(
        ) and user.type not in ProfileType.valid_student_types():
            raise PermissionDenied('You have not the permission to perform this action')

        return DashboardDataFactory().get_dashboard_data_for(user).data
