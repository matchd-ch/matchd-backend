import graphene
from graphene import ObjectType
from graphql_jwt.decorators import login_required

from django.core.exceptions import PermissionDenied

from api.schema.job_posting.schema import JobPosting
from api.schema.challenge.schema import Challenge
from api.schema.match import JobPostingMatchInfo, ChallengeMatchInfo

from db.context.dashboard.dashboard_data_factory import DashboardDataFactory
from db.models import ProfileType


class Dashboard(ObjectType):
    job_postings = graphene.List(graphene.NonNull(JobPosting))
    challenges = graphene.List(graphene.NonNull(Challenge))
    latest_job_postings = graphene.List(graphene.NonNull(JobPosting))
    latest_challenges = graphene.List(graphene.NonNull(Challenge))
    requested_matches = graphene.List(graphene.NonNull(JobPostingMatchInfo))
    unconfirmed_matches = graphene.List(graphene.NonNull(JobPostingMatchInfo))
    confirmed_matches = graphene.List(graphene.NonNull(JobPostingMatchInfo))
    challenge_matches = graphene.List(graphene.NonNull(ChallengeMatchInfo))


class DashboardQuery(ObjectType):
    dashboard = graphene.Field(Dashboard)

    @login_required
    def resolve_dashboard(self, info, **kwargs):
        user = info.context.user

        if user.type not in ProfileType.valid_company_types(
        ) and user.type not in ProfileType.valid_student_types():
            raise PermissionDenied('You have not the permission to perform this action')

        return DashboardDataFactory().get_dashboard_data_for(user).data
