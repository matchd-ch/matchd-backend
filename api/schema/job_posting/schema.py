import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from api.schema.branch import BranchInput
from api.schema.employee import Employee
from api.schema.job_requirement import JobRequirementInput
from api.schema.job_type import JobTypeInput
from api.schema.job_posting_language_relation import JobPostingLanguageRelationInput
from api.schema.registration import EmployeeInput
from api.schema.skill import SkillInput

from db.context.match.match_status import MatchStatus
from db.decorators import job_posting_cheating_protection, hyphenate
from db.exceptions import FormException
from db.forms import process_job_posting_base_data_form, process_job_posting_requirements_form, \
                process_job_posting_allocation_form
from db.models import JobPosting as JobPostingModel, Company, JobPostingState as JobPostingStateModel, ProfileType

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
    skills = graphene.List(graphene.NonNull('api.schema.skill.schema.Skill'))
    branches = graphene.NonNull(graphene.List(graphene.NonNull('api.schema.branch.schema.Branch')))
    languages = graphene.List(
        graphene.NonNull('api.schema.job_posting_language_relation.JobPostingLanguageRelation'))
    title = graphene.NonNull(graphene.String)
    display_title = graphene.NonNull(graphene.String)
    match_status = graphene.Field('api.schema.match.MatchStatus')
    match_hints = graphene.Field('api.schema.match.MatchHints')
    date_created = graphene.Date()
    date_published = graphene.Date()

    class Meta:
        model = JobPostingModel
        interfaces = (relay.Node, )
        fields = (
            'title',
            'description',
            'job_type',
            'workload',
            'company',
            'job_from_date',
            'job_to_date',
            'url',
            'form_step',
            'skills',
            'job_requirements',
            'languages',
            'branches',
            'state',
            'employee',
            'slug',
            'date_published',
            'date_created',
        )
        convert_choices_to_enum = False

    # pylint: disable=W0622
    @classmethod
    @login_required
    def get_node(cls, info, id):
        return get_object_or_404(JobPostingModel, pk=id)

    def resolve_branches(self: JobPostingModel, info):
        return self.branches.all()

    @job_posting_cheating_protection
    def resolve_skills(self: JobPostingModel, info):
        return self.skills.all()

    @job_posting_cheating_protection
    def resolve_languages(self: JobPostingModel, info):
        return self.languages.all()

    def resolve_title(self, info):
        return self.title

    @hyphenate
    def resolve_display_title(self, info):
        return self.title

    def resolve_match_status(self: JobPostingModel, info):
        user = info.context.user

        status = MatchStatus.get(user, job_posting=self)

        if status is not None:
            return {'confirmed': status.complete, 'initiator': status.initiator}
        return None

    def resolve_match_hints(self: JobPostingModel, info):
        user = info.context.user
        if user.type in ProfileType.valid_company_types():
            return None
        return user.student.get_match_hints(self.company)


class JobPostingConnection(relay.Connection):

    class Meta:
        node = JobPosting


class JobPostingQuery(ObjectType):
    job_posting = graphene.Field(JobPosting,
                                 id=graphene.ID(required=False),
                                 slug=graphene.String(required=False))
    job_postings = relay.ConnectionField(JobPostingConnection, slug=graphene.String(required=False))

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

    @login_required
    def resolve_job_postings(self, info, **kwargs):
        user = info.context.user
        slug = kwargs.get('slug')
        if slug is None:
            if user.type in ProfileType.valid_company_types():
                slug = user.company.slug

        company = get_object_or_404(Company, slug=slug)
        # hide incomplete job postings
        # employees should not see job postings which have a DRAFT state
        # eg. an employee should not be able to search with an unpublished job posting
        return JobPostingModel.objects.filter(state=JobPostingState.PUBLIC, company=company)


class JobPostingInputBaseData(graphene.InputObjectType):
    id = graphene.ID(required=False)
    title = graphene.String(description=_('Title'), required=True)
    description = graphene.String(description=_('Description'), required=False)
    job_type = graphene.Field(JobTypeInput, required=True)
    branches = graphene.List(BranchInput, required=True)
    workload = graphene.Int(description=_('Workload'), required=True)
    job_from_date = graphene.String(required=True)
    job_to_date = graphene.String(required=False)
    url = graphene.String(required=False)


class JobPostingBaseDataForm(Output, graphene.Mutation):
    slug = graphene.String()
    job_posting_id = graphene.ID()

    class Arguments:
        base_data = JobPostingInputBaseData(
            description=_('Job Posting Input Base Data is required.'), required=True)

    class Meta:
        description = _('Creates a job posting')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('base_data', None)
        try:
            job_posting = process_job_posting_base_data_form(user, form_data)
        except FormException as exception:
            return JobPostingBaseDataForm(success=False, errors=exception.errors)
        return JobPostingBaseDataForm(success=True,
                                      errors=None,
                                      slug=job_posting.slug,
                                      job_posting_id=job_posting.id)


class JobPostingInputRequirements(graphene.InputObjectType):
    id = graphene.ID()
    job_requirements = graphene.List(JobRequirementInput, required=False)
    skills = graphene.List(SkillInput, required=False)
    languages = graphene.List(JobPostingLanguageRelationInput, required=False)


class JobPostingRequirements(Output, graphene.Mutation):
    slug = graphene.String()
    job_posting_id = graphene.ID()

    class Arguments:
        requirements = JobPostingInputRequirements(
            description=_('Job Posting Input Requirements is required.'), required=True)

    class Meta:
        description = _('Updates a job posting')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('requirements', None)
        try:
            job_posting = process_job_posting_requirements_form(user, form_data)
        except FormException as exception:
            return JobPostingRequirements(success=False, errors=exception.errors)
        return JobPostingRequirements(success=True,
                                      errors=None,
                                      slug=job_posting.slug,
                                      job_posting_id=job_posting.id)


class JobPostingInputAllocation(graphene.InputObjectType):
    id = graphene.ID()
    state = graphene.String(description=_('State'), required=True)
    employee = graphene.Field(EmployeeInput, required=True)


class JobPostingAllocationForm(Output, graphene.Mutation):
    slug = graphene.String()
    job_posting_id = graphene.ID()

    class Arguments:
        allocation = JobPostingInputAllocation(
            description=_('Job Posting Input Allocation is required.'), required=True)

    class Meta:
        description = _('Updates a job posting')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('allocation', None)
        try:
            job_posting = process_job_posting_allocation_form(user, form_data)
        except FormException as exception:
            return JobPostingAllocationForm(success=False, errors=exception.errors)
        return JobPostingAllocationForm(success=True,
                                        errors=None,
                                        slug=job_posting.slug,
                                        job_posting_id=job_posting.id)


class JobPostingMutation(ObjectType):
    job_posting_base_data = JobPostingBaseDataForm.Field()
    job_posting_requirements = JobPostingRequirements.Field()
    job_posting_allocation = JobPostingAllocationForm.Field()
