from django.db.models import Q
from django.conf import settings

from db.context.dashboard.dashboard_data import DashboardData
from db.models.match import Match
from db.models.job_posting import JobPosting, JobPostingState
from db.models.profile_type import ProfileType
from db.models.project_posting import ProjectPosting, ProjectPostingState
from db.models.user import User


class StudentDashboardData(DashboardData):

    def collect_project_postings(self, user: User) -> list[ProjectPosting]:
        return ProjectPosting.objects.filter(student=user.student).order_by('-date_created')

    def collect_latest_job_postings(self, user: User) -> list[ProjectPosting]:
        return JobPosting.objects.filter(
            branches__in=[user.student.branch], state=JobPostingState.PUBLIC).order_by(
                '-date_published')[:settings.DASHBOARD_NUM_LATEST_ENTRIES]

    def collect_latest_project_postings(self, user: User) -> list[ProjectPosting]:
        return ProjectPosting.objects.filter(
            company__isnull=False,
            employee__isnull=False,
            student__isnull=True,
            state=ProjectPostingState.PUBLIC).order_by(
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
                                    project_posting__isnull=True)

    def collect_project_matches(self, user: User) -> list[JobPosting]:
        query = Q(student_confirmed=True, company_confirmed=True, project_posting__isnull=False)
        project_posting_query = Q(project_posting__student=user.student)
        student_query = Q(student=user.student)
        query = query & (project_posting_query | student_query)

        return Match.objects.filter(query)
