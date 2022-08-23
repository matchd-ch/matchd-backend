from django.db.models import Q
from django.conf import settings

from db.context.dashboard.dashboard_data import DashboardData
from db.models.job_posting import JobPosting
from db.models.match import Match
from db.models.profile_type import ProfileType
from db.models.challenge import Challenge, ChallengeState
from db.models.user import User


class CompanyDashboardData(DashboardData):

    def collect_job_postings(self, user: User) -> list[JobPosting]:
        return JobPosting.objects.filter(company=user.company).order_by('-date_created')

    def collect_challenges(self, user: User) -> list[Challenge]:
        return Challenge.objects.filter(company=user.company).order_by('-date_created')

    def collect_latest_challenges(self, user: User) -> list[Challenge]:
        return Challenge.objects.filter(
                company__isnull=True,
                employee__isnull=True, student__isnull=False, state=ChallengeState.PUBLIC). \
                                          order_by('-date_created')[:settings.DASHBOARD_NUM_LATEST_ENTRIES]

    def collect_requested_matches(self, user: User) -> list[Match]:
        return Match.objects.filter(job_posting__company=user.company,
                                    initiator=user.type,
                                    student_confirmed=False,
                                    company_confirmed=True)

    def collect_unconfirmed_matches(self, user: User) -> list[Match]:
        return Match.objects.filter(job_posting__company=user.company,
                                    initiator__in=ProfileType.valid_student_types(),
                                    company_confirmed=False,
                                    student_confirmed=True)

    def collect_confirmed_matches(self, user: User) -> list[Match]:
        return Match.objects.filter(job_posting__company=user.company,
                                    student_confirmed=True,
                                    company_confirmed=True,
                                    challenge__isnull=True)

    def collect_challenge_matches(self, user: User) -> list[JobPosting]:
        query = Q(student_confirmed=True, company_confirmed=True, challenge__isnull=False)
        challenge_query = Q(challenge__company=user.company)
        company_query = Q(company=user.company)
        query = query & (challenge_query | company_query)

        return Match.objects.filter(query)
