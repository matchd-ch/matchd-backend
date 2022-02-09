from django.db.models import Q
from django.conf import settings

from db.context.dashboard.dashboard_data import DashboardData
from db.models.job_posting import JobPosting
from db.models.match import Match
from db.models.profile_type import ProfileType
from db.models.project_posting import ProjectPosting, ProjectPostingState
from db.models.user import User


class CompanyDashboardData(DashboardData):

    def collect_job_postings(self, user: User) -> list[JobPosting]:
        return JobPosting.objects.filter(company=user.company).order_by('-date_created')

    def collect_project_postings(self, user: User) -> list[ProjectPosting]:
        return ProjectPosting.objects.filter(company=user.company).order_by('-date_created')

    def collect_latest_project_postings(self, user: User) -> list[ProjectPosting]:
        return ProjectPosting.objects.filter(
                company__isnull=True,
                employee__isnull=True, student__isnull=False, state=ProjectPostingState.PUBLIC). \
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
                                    project_posting__isnull=True)

    def collect_project_matches(self, user: User) -> list[JobPosting]:
        query = Q(student_confirmed=True, company_confirmed=True, project_posting__isnull=False)
        project_posting_query = Q(project_posting__company=user.company)
        company_query = Q(company=user.company)
        query = query & (project_posting_query | company_query)

        return Match.objects.filter(query)
