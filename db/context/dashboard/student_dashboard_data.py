from django.db.models import Q
from django.conf import settings

from db.context.dashboard.dashboard_data import DashboardData
from db.models.match import Match
from db.models.job_posting import JobPosting, JobPostingState
from db.models.profile_type import ProfileType
from db.models.challenge import Challenge, ChallengeState
from db.models.user import User


class StudentDashboardData(DashboardData):

    def collect_challenges(self, user: User) -> list[Challenge]:
        return Challenge.objects.filter(student=user.student).order_by('-date_created')

    def collect_latest_job_postings(self, user: User) -> list[Challenge]:
        return JobPosting.objects.filter(
            branches__in=[user.student.branch], state=JobPostingState.PUBLIC).order_by(
                '-date_published')[:settings.DASHBOARD_NUM_LATEST_ENTRIES]

    def collect_latest_challenges(self, user: User) -> list[Challenge]:
        return Challenge.objects.filter(company__isnull=False,
                                        employee__isnull=False,
                                        student__isnull=True,
                                        state=ChallengeState.PUBLIC).order_by(
                                            '-date_created')[:settings.DASHBOARD_NUM_LATEST_ENTRIES]

    def collect_requested_matches(self, user: User) -> list[Match]:
        return Match.objects.filter(student=user.student,
                                    initiator=user.type,
                                    company_confirmed=False,
                                    student_confirmed=True)

    def collect_unconfirmed_matches(self, user: User) -> list[Match]:
        return Match.objects.filter(student=user.student,
                                    initiator__in=ProfileType.valid_company_types(),
                                    student_confirmed=False,
                                    company_confirmed=True)

    def collect_confirmed_matches(self, user: User) -> list[Match]:
        return Match.objects.filter(student=user.student,
                                    student_confirmed=True,
                                    company_confirmed=True,
                                    challenge__isnull=True)

    def collect_challenge_matches(self, user: User) -> list[JobPosting]:
        query = Q(student_confirmed=True, company_confirmed=True, challenge__isnull=False)
        challenge_query = Q(challenge__student=user.student)
        student_query = Q(student=user.student)
        query = query & (challenge_query | student_query)

        return Match.objects.filter(query)
