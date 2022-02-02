import graphene
from graphene import ObjectType

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from api.schema.job_posting.schema import JobPosting
from api.schema.match import JobPostingMatchInfo, ProjectPostingMatchInfo
from api.schema.project_posting.schema import ProjectPosting, ProjectPostingState
from db.models import ProfileType, JobPosting as JobPostingModel, JobPostingState, Match, \
    ProjectPosting as ProjectPostingModel


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

    def resolve_dashboard(self, info, **kwargs):
        user = info.context.user

        if not user.is_authenticated:
            raise PermissionDenied('You have not the permission to perform this action')

        if user.type not in ProfileType.valid_company_types(
        ) and user.type not in ProfileType.valid_student_types():
            raise PermissionDenied('You have not the permission to perform this action')

        job_postings = None
        project_postings = None
        latest_job_postings = None
        latest_project_postings = None
        requested_matches = None
        unconfirmed_matches = None
        confirmed_matches = None
        project_matches = None
        if user.type in ProfileType.valid_company_types():
            job_postings = JobPostingModel.objects.filter(
                company=user.company).order_by('-date_created')
            project_postings = ProjectPostingModel.objects.filter(
                company=user.company).order_by('-date_created')
            latest_job_postings = None
            latest_project_postings = ProjectPostingModel.objects.filter(
                company__isnull=True,
                employee__isnull=True, student__isnull=False, state=ProjectPostingState.PUBLIC). \
                                          order_by('-date_created')[:settings.DASHBOARD_NUM_LATEST_ENTRIES]
            requested_matches = Match.objects.filter(job_posting__company=user.company,
                                                     initiator=user.type,
                                                     student_confirmed=False,
                                                     company_confirmed=True)
            unconfirmed_matches = Match.objects.filter(
                job_posting__company=user.company,
                initiator__in=ProfileType.valid_student_types(),
                company_confirmed=False,
                student_confirmed=True)
            confirmed_matches = Match.objects.filter(job_posting__company=user.company,
                                                     student_confirmed=True,
                                                     company_confirmed=True,
                                                     project_posting__isnull=True)
            query = Q(student_confirmed=True, company_confirmed=True, project_posting__isnull=False)
            project_posting_query = Q(project_posting__company=user.company)
            company_query = Q(company=user.company)
            query = query & (project_posting_query | company_query)
            project_matches = Match.objects.filter(query)
        if user.type in ProfileType.valid_student_types():
            job_postings = None
            project_postings = ProjectPostingModel.objects.filter(
                student=user.student).order_by('-date_created')
            latest_job_postings = JobPostingModel.objects.filter(
                branches__in=[user.student.branch], state=JobPostingState.PUBLIC). \
                                      order_by('-date_published')[:settings.DASHBOARD_NUM_LATEST_ENTRIES]
            latest_project_postings = ProjectPostingModel.objects.filter(
                company__isnull=False,
                employee__isnull=False, student__isnull=True, state=ProjectPostingState.PUBLIC). \
                                          order_by('-date_created')[:settings.DASHBOARD_NUM_LATEST_ENTRIES]
            requested_matches = Match.objects.filter(student=user.student,
                                                     initiator=user.type,
                                                     company_confirmed=False,
                                                     student_confirmed=True)
            unconfirmed_matches = Match.objects.filter(
                student=user.student,
                initiator__in=ProfileType.valid_company_types(),
                student_confirmed=False,
                company_confirmed=True)
            confirmed_matches = Match.objects.filter(student=user.student,
                                                     student_confirmed=True,
                                                     company_confirmed=True,
                                                     project_posting__isnull=True)
            query = Q(student_confirmed=True, company_confirmed=True, project_posting__isnull=False)
            project_posting_query = Q(project_posting__student=user.student)
            student_query = Q(student=user.student)
            query = query & (project_posting_query | student_query)
            project_matches = Match.objects.filter(query)

        return {
            'job_postings': job_postings,
            'project_postings': project_postings,
            'latest_job_postings': latest_job_postings,
            'latest_project_postings': latest_project_postings,
            'requested_matches': requested_matches,
            'unconfirmed_matches': unconfirmed_matches,
            'confirmed_matches': confirmed_matches,
            'project_matches': project_matches
        }
