import graphene
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from graphene import ObjectType
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from api.schema.branch import BranchInput
from api.schema.expectation import ExpectationInput
from api.schema.job_option import JobOptionInput
from api.schema.job_posting_language_relation import JobPostingLanguageRelationInput
from api.schema.registration import EmployeeInput
from api.schema.skill import SkillInput
from db.exceptions import FormException
from db.forms import process_job_posting_form_step_1, process_job_posting_form_step_2, process_job_posting_form_step_3
from db.models import JobPosting as JobPostingModel, Company, JobPostingState as JobPostingStateModel

JobPostingState = graphene.Enum.from_enum(JobPostingStateModel)


class JobPosting(DjangoObjectType):
    state = graphene.Field(JobPostingState)

    class Meta:
        model = JobPostingModel
        fields = ('id', 'description', 'job_option', 'workload', 'company', 'job_from_date', 'job_to_date', 'url',
                  'form_step', 'skills', 'expectations', 'languages', 'branch', 'state', 'employee', )
        convert_choices_to_enum = False


class JobPostingQuery(ObjectType):
    job_postings = graphene.List(JobPosting, company=graphene.Int(required=True))
    job_posting = graphene.Field(JobPosting, id=graphene.ID(required=True))

    def resolve_job_postings(self, info, **kwargs):
        company_id = kwargs.get('company')
        company = get_object_or_404(Company, pk=company_id)

        # show incomplete job postings for owner
        if info.context.user.company == company:
            return JobPostingModel.objects.filter(company=company)

        # hide incomplete job postings for other users
        return JobPostingModel.objects.filter(state=JobPostingState.PUBLIC, company=company)

    def resolve_job_posting(self, info, **kwargs):
        job_posting_id = kwargs.get('id')
        job_posting = get_object_or_404(JobPostingModel, id=job_posting_id)

        # show incomplete job postings for owner
        if info.context.user.company == job_posting.company:
            return job_posting

        # hide incomplete job postings for other users
        if job_posting.state != JobPostingState.PUBLIC:
            raise Http404(_('Job posting not found'))
        return job_posting


class JobPostingInputStep1(graphene.InputObjectType):
    id = graphene.ID(required=False)
    description = graphene.String(description=_('Description'), required=True)
    job_option = graphene.Field(JobOptionInput, required=True)
    branch = graphene.Field(BranchInput, required=True)
    workload = graphene.Int(description=_('Workload'), required=True)
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
    expectations = graphene.List(ExpectationInput, required=False)
    skills = graphene.List(SkillInput, required=False)
    languages = graphene.List(JobPostingLanguageRelationInput, required=False)


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


class JobPostingInputStep3(graphene.InputObjectType):
    id = graphene.ID()
    state = graphene.String(description=_('State'), required=True)
    employee = graphene.Field(EmployeeInput, required=True)


class JobPostingStep3(Output, graphene.Mutation):
    job_posting_id = graphene.ID()

    class Arguments:
        step3 = JobPostingInputStep3(description=_('Job Posting Input Step 3 is required.'), required=True)

    class Meta:
        description = _('Updates a job posting')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('step3', None)
        try:
            job_posting = process_job_posting_form_step_3(user, form_data)
        except FormException as exception:
            return JobPostingStep3(success=False, errors=exception.errors)
        return JobPostingStep3(success=True, errors=None, job_posting_id=job_posting.id)


class JobPostingMutation(graphene.ObjectType):
    job_posting_step_1 = JobPostingStep1.Field()
    job_posting_step_2 = JobPostingStep2.Field()
    job_posting_step_3 = JobPostingStep3.Field()
