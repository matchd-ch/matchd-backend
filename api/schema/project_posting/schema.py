import graphene
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from graphene import ObjectType
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from api.schema.employee import Employee, EmployeeInput
from api.schema.keyword.schema import KeywordInput
from api.schema.project_type.schema import ProjectTypeInput
from api.schema.topic.schema import TopicInput
from db.decorators import hyphenate
from db.exceptions import FormException
from db.forms import process_project_posting_form_step_1, process_project_posting_form_step_2
from db.models import ProjectPosting as ProjectPostingModel, ProjectPostingState as ProjectPostingStateModel, \
    ProfileType, Match as MatchModel

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

    class Meta:
        model = ProjectPostingModel
        fields = ('id', 'title', 'description', 'project_type', 'topic', 'company', 'keywords',
                  'additional_information', 'website', 'project_from_date', 'form_step', 'state', 'date_published',
                  'date_created', 'student', 'employee', 'slug',)
        convert_choices_to_enum = False

    def resolve_keywords(self: ProjectPostingModel, info):
        return self.keywords.all()

    def resolve_title(self, info):
        return self.title

    @hyphenate
    def resolve_display_title(self, info):
        return self.title

    def resolve_match_status(self: ProjectPostingModel, info):
        user = info.context.user
        status = None
        if user.type in ProfileType.valid_student_types():
            try:
                status = MatchModel.objects.get(project_posting=self, student=user.student)
            except MatchModel.DoesNotExist:
                pass
        if user.type in ProfileType.valid_company_types():
            try:
                status = MatchModel.objects.get(project_posting=self, company=user.company)
            except MatchModel.DoesNotExist:
                pass

        if status is not None:
            return {
                'confirmed':  status.complete,
                'initiator': status.initiator
            }
        return None

    def resolve_match_hints(self: ProjectPostingModel, info):
        user = info.context.user
        exists = False
        if user.type in ProfileType.valid_student_types():
            try:
                exists = MatchModel.objects.filter(project_posting=self, student=user.student).exists()
            except MatchModel.DoesNotExist:
                pass
        return {
            'has_confirmed_match': False,
            'has_requested_match': exists
        }


class ProjectPostingQuery(ObjectType):
    project_posting = graphene.Field(ProjectPosting, id=graphene.ID(required=False),
                                     slug=graphene.String(required=False))
    project_postings = graphene.List(ProjectPosting)

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

        # show incomplete project postings for employees of the company
        user = info.context.user
        if user.type in ProfileType.valid_company_types():
            # noinspection PyUnboundLocalVariable
            if user.company == project_posting.company:
                return project_posting

        # show incomplete project postings if student is owner
        if user.type in ProfileType.valid_student_types():
            if user.student == project_posting.student:
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


class ProjectPostingInputStep1(graphene.InputObjectType):
    id = graphene.ID(required=False)
    title = graphene.String(description=_('Title'), required=True)
    project_type = graphene.Field(ProjectTypeInput, required=True)
    topic = graphene.Field(TopicInput, required=True)
    keywords = graphene.List(KeywordInput, required=False)
    description = graphene.String(description=_('Description'), required=True)
    additional_information = graphene.String(description=_('Additional Information'), required=False)
    project_from_date = graphene.String(required=False)
    website = graphene.String(required=False)


class ProjectPostingStep1(Output, graphene.Mutation):
    slug = graphene.String()
    project_posting_id = graphene.ID()

    class Arguments:
        step1 = ProjectPostingInputStep1(description=_('Project Posting Input Step 1 is required.'), required=True)

    class Meta:
        description = _('Creates a project posting')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('step1', None)
        try:
            project_posting = process_project_posting_form_step_1(user, form_data)
        except FormException as exception:
            return ProjectPostingStep1(success=False, errors=exception.errors)
        return ProjectPostingStep1(success=True, errors=None, slug=project_posting.slug,
                                   project_posting_id=project_posting.id)


class ProjectPostingInputStep2(graphene.InputObjectType):
    id = graphene.ID()
    state = graphene.String(description=_('State'), required=True)
    employee = graphene.Field(EmployeeInput, required=False)


class ProjectPostingStep2(Output, graphene.Mutation):
    slug = graphene.String()
    project_posting_id = graphene.ID()

    class Arguments:
        step2 = ProjectPostingInputStep2(description=_('Project Posting Input Step 2 is required.'), required=True)

    class Meta:
        description = _('Updates a project posting')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('step2', None)
        try:
            project_posting = process_project_posting_form_step_2(user, form_data)
        except FormException as exception:
            return ProjectPostingStep2(success=False, errors=exception.errors)
        return ProjectPostingStep2(success=True, errors=None, slug=project_posting.slug,
                                   project_posting_id=project_posting.id)


class ProjectPostingMutation(graphene.ObjectType):
    project_posting_step_1 = ProjectPostingStep1.Field()
    project_posting_step_2 = ProjectPostingStep2.Field()
