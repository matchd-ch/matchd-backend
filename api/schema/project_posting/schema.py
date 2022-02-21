import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from api.schema.employee import Employee, EmployeeInput
from api.schema.keyword.schema import KeywordInput
from api.schema.project_type.schema import ProjectTypeInput
from api.schema.topic.schema import TopicInput

from db.context.match.match_status import MatchStatus
from db.decorators import hyphenate
from db.exceptions import FormException
from db.forms import process_project_posting_base_data_form, process_project_posting_specific_data_form
from db.forms.project_posting_allocation import process_project_posting_allocation_form
from db.models import ProjectPosting as ProjectPostingModel, ProjectPostingState as ProjectPostingStateModel, \
    ProfileType

ProjectPostingState = graphene.Enum.from_enum(ProjectPostingStateModel)


class ProjectPostingInput(graphene.InputObjectType):
    id = graphene.ID(required=True)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id


class ProjectPosting(DjangoObjectType):
    title = graphene.NonNull(graphene.String)
    display_title = graphene.NonNull(graphene.String)
    state = graphene.Field(graphene.NonNull(ProjectPostingState))
    employee = graphene.Field(Employee)
    keywords = graphene.List(graphene.NonNull('api.schema.keyword.schema.Keyword'))
    match_status = graphene.Field('api.schema.match.MatchStatus')
    match_hints = graphene.Field('api.schema.match.MatchHints')
    date_created = graphene.Date()
    date_published = graphene.Date()

    class Meta:
        model = ProjectPostingModel
        interfaces = (relay.Node, )
        fields = (
            'title',
            'description',
            'project_type',
            'topic',
            'company',
            'keywords',
            'additional_information',
            'website',
            'project_from_date',
            'form_step',
            'state',
            'date_published',
            'date_created',
            'student',
            'employee',
            'slug',
        )
        convert_choices_to_enum = False

    # pylint: disable=W0622
    @classmethod
    @login_required
    def get_node(cls, info, id):
        return get_object_or_404(ProjectPostingModel, pk=id)

    def resolve_keywords(self: ProjectPostingModel, info):
        return self.keywords.all()

    def resolve_title(self, info):
        return self.title

    @hyphenate
    def resolve_display_title(self, info):
        return self.title

    def resolve_match_status(self: ProjectPostingModel, info):
        user = info.context.user

        status = MatchStatus.get(user, project_posting=self)

        if status is not None:
            return {'confirmed': status.complete, 'initiator': status.initiator}
        return None

    def resolve_match_hints(self: ProjectPostingModel, info):
        user = info.context.user
        if user.type in ProfileType.valid_company_types():
            return None
        if self.company is None:
            return None
        return user.student.get_match_hints(self.company)


class ProjectPostingConnection(relay.Connection):

    class Meta:
        node = ProjectPosting


class ProjectPostingQuery(ObjectType):
    project_posting = graphene.Field(ProjectPosting,
                                     id=graphene.ID(required=False),
                                     slug=graphene.String(required=False))
    project_postings = relay.ConnectionField(ProjectPostingConnection)

    @login_required
    def resolve_project_posting(self, info, **kwargs):
        slug = kwargs.get('slug')
        project_posting_id = kwargs.get('id')

        if slug is None and project_posting_id is None:
            raise Http404(_('Project posting not found'))

        if slug is not None:
            project_posting = get_object_or_404(ProjectPostingModel, slug=slug)
        elif project_posting_id is not None:
            project_posting = get_object_or_404(ProjectPostingModel, pk=project_posting_id)

        user = info.context.user
        # show incomplete project postings for employees of the company
        if user.type in ProfileType.valid_company_types(
        ) and user.company == project_posting.company:
            return project_posting

        # show incomplete project postings if student is owner
        if user.type in ProfileType.valid_student_types(
        ) and user.student == project_posting.student:
            return project_posting

        # hide incomplete project postings for other users
        if project_posting.state != ProjectPostingState.PUBLIC:
            raise Http404(_('Project posting not found'))
        return project_posting

    @login_required
    def resolve_project_postings(self, info, **kwargs):
        user = info.context.user
        project_postings = None
        if user.type in ProfileType.valid_company_types():
            project_postings = ProjectPostingModel.objects.filter(company=user.company,
                                                                  state=ProjectPostingState.PUBLIC)
        if user.type in ProfileType.valid_student_types():
            project_postings = ProjectPostingModel.objects.filter(student=user.student,
                                                                  state=ProjectPostingState.PUBLIC)
        return project_postings


class ProjectPostingInputBaseData(graphene.InputObjectType):
    id = graphene.ID(required=False)
    title = graphene.String(description=_('Title'), required=True)
    project_type = graphene.Field(ProjectTypeInput, required=True)
    topic = graphene.Field(TopicInput, required=True)
    keywords = graphene.List(KeywordInput, required=False)
    description = graphene.String(description=_('Description'), required=True)
    additional_information = graphene.String(description=_('Additional Information'),
                                             required=False)


class ProjectPostingBaseData(Output, graphene.Mutation):
    slug = graphene.String()
    project_posting_id = graphene.ID()

    class Arguments:
        base_data = ProjectPostingInputBaseData(
            description=_('Project Posting Input Base Data is required.'), required=True)

    class Meta:
        description = _('Creates a project posting')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('base_data', None)
        try:
            project_posting = process_project_posting_base_data_form(user, form_data)
        except FormException as exception:
            return ProjectPostingBaseData(success=False, errors=exception.errors)
        return ProjectPostingBaseData(success=True,
                                      errors=None,
                                      slug=project_posting.slug,
                                      project_posting_id=project_posting.id)


class ProjectPostingInputSpecificData(graphene.InputObjectType):
    id = graphene.ID(required=False)
    project_from_date = graphene.String(required=False)
    website = graphene.String(required=False)


class ProjectPostingSpecificData(Output, graphene.Mutation):
    slug = graphene.String()
    project_posting_id = graphene.ID()

    class Arguments:
        specific_data = ProjectPostingInputSpecificData(
            description=_('Project Posting Input Specific Data is required.'), required=True)

    class Meta:
        description = _('Creates a project posting')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('specific_data', None)
        try:
            project_posting = process_project_posting_specific_data_form(user, form_data)
        except FormException as exception:
            return ProjectPostingSpecificData(success=False, errors=exception.errors)
        return ProjectPostingSpecificData(success=True,
                                          errors=None,
                                          slug=project_posting.slug,
                                          project_posting_id=project_posting.id)


class ProjectPostingInputAllocation(graphene.InputObjectType):
    id = graphene.ID()
    state = graphene.String(description=_('State'), required=True)
    employee = graphene.Field(EmployeeInput, required=False)


class ProjectPostingAllocation(Output, graphene.Mutation):
    slug = graphene.String()
    project_posting_id = graphene.ID()

    class Arguments:
        allocation = ProjectPostingInputAllocation(
            description=_('Project Posting Input Allocation is required.'), required=True)

    class Meta:
        description = _('Updates a project posting')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('allocation', None)
        try:
            project_posting = process_project_posting_allocation_form(user, form_data)
        except FormException as exception:
            return ProjectPostingAllocation(success=False, errors=exception.errors)
        return ProjectPostingAllocation(success=True,
                                        errors=None,
                                        slug=project_posting.slug,
                                        project_posting_id=project_posting.id)


class ProjectPostingMutation(ObjectType):
    project_posting_base_data = ProjectPostingBaseData.Field()
    project_posting_specific_data = ProjectPostingSpecificData.Field()
    project_posting_allocation = ProjectPostingAllocation.Field()
