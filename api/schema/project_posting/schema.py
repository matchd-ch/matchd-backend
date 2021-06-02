import graphene
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from graphene import ObjectType
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from api.schema.employee import Employee
from db.decorators import hyphenate
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
    # match_hints = graphene.Field('api.schema.match.MatchHints')

    class Meta:
        model = ProjectPostingModel
        fields = ('id', 'title', 'description', 'project_type', 'topic', 'company', 'keywords',
                  'additional_information', 'website', 'project_from_date', 'form_step', 'state', 'date_published',
                  'date_created', 'student', 'employee' )
        convert_choices_to_enum = False

    def resolve_keywords(self: ProjectPostingModel, info):
        return self.keywords.all()

    def resolve_title(self, info):
        return self.title

    @hyphenate
    def resolve_display_title(self, info):
        return self.title

    def resolve_match_status(self: ProjectPostingModel, info):
        # todo
        return {
            'confirmed': False,
            'initiator': ProfileType.STUDENT
        }
        # user = info.context.user
        # status = None
        # if user.type in ProfileType.valid_student_types():
        #     try:
        #         status = MatchModel.objects.get(job_posting=self, student=user.student)
        #     except MatchModel.DoesNotExist:
        #         pass
        #
        # if status is not None:
        #     return {
        #         'confirmed':  status.complete,
        #         'initiator': status.initiator
        #     }
        # return None

    def resolve_match_hints(self: ProjectPostingModel, info):
        user = info.context.user
        # todo
        return {
            'has_confirmed_match': False,
            'has_requested_match': False
        }


class ProjectPostingQuery(ObjectType):
    project_posting = graphene.Field(ProjectPosting, id=graphene.ID(required=False),
                                     slug=graphene.String(required=False))

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

        # show incomplete job postings for employees of the company
        # noinspection PyUnboundLocalVariable
        if info.context.user.company == project_posting.company:
            return project_posting

        # hide incomplete job postings for other users
        if project_posting.state != ProjectPostingState.PUBLIC:
            raise Http404(_('Project posting not found'))
        return project_posting
