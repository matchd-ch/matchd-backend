import graphene
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from graphene import ObjectType
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from api.schema.branch import BranchInputType
from api.schema.expectation import ExpectationInputType
from api.schema.job_option import JobOptionInputType
from api.schema.job_posting_language_relation import JobPostingLanguageRelationInputType
from api.schema.skill import SkillInputType
from db.exceptions import FormException
from db.forms import process_job_posting_form_step_1, process_job_posting_form_step_2
from db.models import JobPosting, Company


class JobPostingType(DjangoObjectType):
    class Meta:
        model = JobPosting
        fields = ('id', 'description', 'job_option', 'workload', 'company', 'job_from_date', 'job_to_date', 'url',
                  'form_step', 'skills', 'expectations', 'languages')


class JobPostingQuery(ObjectType):
    job_postings = graphene.List(JobPostingType, company=graphene.Int(required=True))
    job_posting = graphene.Field(JobPostingType, id=graphene.Int(required=True))

    def resolve_job_postings(self, info, **kwargs):
        company_id = kwargs.get('company')
        company = get_object_or_404(Company, pk=company_id)

        # show incomplete job postings for owner
        if info.context.user.company == company:
            return JobPosting.objects.filter(company=company)

        # hide incomplete job postings for other users
        return JobPosting.objects.filter(form_step=3, company=company)

    def resolve_job_posting(self, info, **kwargs):
        job_posting_id = kwargs.get('id')
        job_posting = get_object_or_404(JobPosting, id=job_posting_id)

        # show incomplete job postings for owner
        if info.context.user.company == job_posting.company:
            return job_posting

        # hide incomplete job postings for other users
        if job_posting.form_step < 3:
            raise Http404(_('Job posting not found'))
        return job_posting


class JobPostingInputStep1(graphene.InputObjectType):
    description = graphene.String(description=_('Description'), required=True)
    job_option = graphene.Field(JobOptionInputType, required=True)
    branch = graphene.Field(BranchInputType, required=True)
    workload = graphene.String(description=_('Workload'), required=False)
    job_from_date = graphene.String(required=True)
    job_to_date = graphene.String(required=False)
    url = graphene.String(required=False)


class JobPostingStep1(Output, graphene.Mutation):

    job_posting_id = graphene.ID()

    class Arguments:
        step1 = JobPostingInputStep1(description=_('Job Posting Input Step 1 is required.'), required=True)

    class Meta:
        description = _('Creates a job posting')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('step1', None)
        try:
            job_posting = process_job_posting_form_step_1(user, form_data)
        except FormException as exception:
            return JobPostingStep1(success=False, errors=exception.errors)
        return JobPostingStep1(success=True, errors=None, job_posting_id=job_posting.id)


class JobPostingInputStep2(graphene.InputObjectType):
    id = graphene.ID()
    expectations = graphene.List(ExpectationInputType, required=False)
    skills = graphene.List(SkillInputType, required=False)
    languages = graphene.List(JobPostingLanguageRelationInputType, required=False)


class JobPostingStep2(Output, graphene.Mutation):
    job_posting_id = graphene.ID()

    class Arguments:
        step2 = JobPostingInputStep2(description=_('Job Posting Input Step 2 is required.'), required=True)

    class Meta:
        description = _('Updates a job posting')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('step2', None)
        try:
            job_posting = process_job_posting_form_step_2(user, form_data)
        except FormException as exception:
            return JobPostingStep2(success=False, errors=exception.errors)
        return JobPostingStep2(success=True, errors=None, job_posting_id=job_posting.id)


class JobPostingMutation(graphene.ObjectType):
    job_posting_step_1 = JobPostingStep1.Field()
    job_posting_step_2 = JobPostingStep2.Field()
