import graphene
from django.conf import settings
from graphene import ObjectType

from api.schema.job_posting.schema import JobPosting
from api.schema.match import MatchInfo
from db.models import ProfileType, JobPosting as JobPostingModel, JobPostingState, Match


class Dashboard(ObjectType):
    job_postings = graphene.List(graphene.NonNull(JobPosting))
    requested_matches = graphene.List(graphene.NonNull(MatchInfo))
    unconfirmed_matches = graphene.List(graphene.NonNull(MatchInfo))
    confirmed_matches = graphene.List(graphene.NonNull(MatchInfo))


class DashboardQuery(ObjectType):
    dashboard = graphene.Field(Dashboard)

    def resolve_dashboard(self, info, **kwargs):
        user = info.context.user

        job_postings = None
        requested_matches = None
        unconfirmed_matches = None
        confirmed_matches = None
        if user.type in ProfileType.valid_company_types():
            job_postings = JobPostingModel.objects.filter(company=user.company).order_by('-date_created')
            requested_matches = Match.objects.filter(job_posting__company=user.company, initiator=user.type,
                                                     student_confirmed=False, company_confirmed=True)
            unconfirmed_matches = Match.objects.filter(job_posting__company=user.company, initiator=ProfileType.STUDENT,
                                                       company_confirmed=False, student_confirmed=True)
            confirmed_matches = Match.objects.filter(job_posting__company=user.company, student_confirmed=True,
                                                     company_confirmed=True)
        if user.type in ProfileType.valid_student_types():
            job_postings = JobPostingModel.objects.filter(branch=user.student.branch, state=JobPostingState.PUBLIC).\
                order_by('-date_published')[:settings.DASHBOARD_STUDENT_NUM_JOB_POSTINGS]
            requested_matches = Match.objects.filter(student=user.student, initiator=user.type,
                                                       company_confirmed=False, student_confirmed=True)
            unconfirmed_matches = Match.objects.filter(student=user.student, initiator=ProfileType.COMPANY,
                                                       student_confirmed=False, company_confirmed=True)
            confirmed_matches = Match.objects.filter(student=user.student, student_confirmed=True,
                                                     company_confirmed=True)

        return {
            'job_postings': job_postings,
            'requested_matches': requested_matches,
            'unconfirmed_matches': unconfirmed_matches,
            'confirmed_matches': confirmed_matches
        }
