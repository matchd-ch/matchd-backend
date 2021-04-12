import graphene
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from graphene import ObjectType
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from api.helper import is_me_query
from api.schema.branch import BranchInput
from api.schema.employee import Employee
from api.schema.job_requirement import JobRequirementInput
from api.schema.job_type import JobTypeInput
from api.schema.job_posting_language_relation import JobPostingLanguageRelationInput
from api.schema.registration import EmployeeInput
from api.schema.skill import SkillInput
from db.exceptions import FormException
from db.forms import process_job_posting_form_step_1, process_job_posting_form_step_2, process_job_posting_form_step_3
from db.models import JobPosting as JobPostingModel, Company, JobPostingState as JobPostingStateModel

JobPostingState = graphene.Enum.from_enum(JobPostingStateModel)


class JobPostingInput(graphene.InputObjectType):
    id = graphene.ID(required=True)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id


class JobPosting(DjangoObjectType):
    state = graphene.Field(graphene.NonNull(JobPostingState))
    employee = graphene.Field(Employee)
    workload = graphene.Field(graphene.NonNull(graphene.Int))
    skills = graphene.NonNull(graphene.List(graphene.NonNull('api.schema.skill.schema.Skill')))
    languages = graphene.NonNull(graphene.List(graphene.NonNull(
        'api.schema.job_posting_language_relation.JobPostingLanguageRelation')))

    class Meta:
        model = JobPostingModel
        fields = ('id', 'title', 'description', 'job_type', 'workload', 'company', 'job_from_date', 'job_to_date',
                  'url', 'form_step', 'skills', 'job_requirements', 'languages', 'branch', 'state', 'employee', 'slug')
        convert_choices_to_enum = False

    def resolve_skills(self: JobPostingModel, info):
        if is_me_query(info):
            return self.skills.all()
        return []

    def resolve_languages(self: JobPostingModel, info):
        if is_me_query(info):
            return self.languages.all()
        return []


class JobPostingQuery(ObjectType):
    job_postings = graphene.List(JobPosting, slug=graphene.String(required=False))
    job_posting = graphene.Field(JobPosting, id=graphene.ID(required=False), slug=graphene.String(required=False))

    @login_required
    def resolve_job_postings(self, info, **kwargs):
        slug = kwargs.get('slug')
        company = get_object_or_404(Company, slug=slug)
        # hide incomplete job postings
        # employees should not see job postings which have a DRAFT state
        # eg. an employee should not be able to search with an unpublished job posting
        return JobPostingModel.objects.filter(state=JobPostingState.PUBLIC, company=company)

    @login_required
    def resolve_job_posting(self, info, **kwargs):
        slug = kwargs.get('slug')
        job_posting_id = kwargs.get('id')
        if slug is None and job_posting_id is None:
            raise Http404(_('Job posting not found'))
        if slug is not None:
            job_posting = get_object_or_404(JobPostingModel, slug=slug)
        elif job_posting_id is not None:
            job_posting = get_object_or_404(JobPostingModel, pk=job_posting_id)

        # show incomplete job postings for employees of the company
        # noinspection PyUnboundLocalVariable
        if info.context.user.company == job_posting.company:
            return job_posting

        # hide incomplete job postings for other users
        if job_posting.state != JobPostingState.PUBLIC:
            raise Http404(_('Job posting not found'))
        return job_posting


class JobPostingInputStep1(graphene.InputObjectType):
    id = graphene.ID(required=False)
    title = graphene.String(description=_('Title'), required=True)
    description = graphene.String(description=_('Description'), required=True)
    job_type = graphene.Field(JobTypeInput, required=True)
    branch = graphene.Field(BranchInput, required=True)
    workload = graphene.Int(description=_('Workload'), required=True)
    job_from_date = graphene.String(required=True)
    job_to_date = graphene.String(required=False)
    url = graphene.String(required=False)


class JobPostingStep1(Output, graphene.Mutation):
    slug = graphene.String()

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
        return JobPostingStep1(success=True, errors=None, slug=job_posting.slug)


class JobPostingInputStep2(graphene.InputObjectType):
    id = graphene.ID()
    job_requirements = graphene.List(JobRequirementInput, required=False)
    skills = graphene.List(SkillInput, required=False)
    languages = graphene.List(JobPostingLanguageRelationInput, required=False)


class JobPostingStep2(Output, graphene.Mutation):
    slug = graphene.String()

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
        return JobPostingStep2(success=True, errors=None, slug=job_posting.slug)


class JobPostingInputStep3(graphene.InputObjectType):
    id = graphene.ID()
    state = graphene.String(description=_('State'), required=True)
    employee = graphene.Field(EmployeeInput, required=True)


class JobPostingStep3(Output, graphene.Mutation):
    slug = graphene.String()

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
        return JobPostingStep3(success=True, errors=None, slug=job_posting.slug)


class JobPostingMutation(graphene.ObjectType):
    job_posting_step_1 = JobPostingStep1.Field()
    job_posting_step_2 = JobPostingStep2.Field()
    job_posting_step_3 = JobPostingStep3.Field()
