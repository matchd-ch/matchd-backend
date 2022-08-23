import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphql_relay import to_global_id
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from api.helper import extract_ids, resolve_node_id, resolve_node_ids
from api.schema.employee import Employee, EmployeeInput
from api.schema.keyword.schema import KeywordInput
from api.schema.challenge_type.schema import ChallengeTypeInput

from db.context.match.match_status import MatchStatus
from db.decorators import hyphenate, restrict_challenge, restrict_challenge_node
from db.exceptions import FormException
from db.forms import process_challenge_base_data_form, process_challenge_specific_data_form
from db.forms.challenge_allocation import process_challenge_allocation_form
from db.models import Challenge as ChallengeModel, ChallengeState as ChallengeStateModel, \
    ProfileType
from db.search.challenge.challenge_search import search_challenge

# pylint: disable=W0221

ChallengeState = graphene.Enum.from_enum(ChallengeStateModel)


class ChallengeInput(graphene.InputObjectType):
    id = graphene.String(required=True)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id


class Challenge(DjangoObjectType):
    avatar_url = graphene.String()
    title = graphene.NonNull(graphene.String)
    display_title = graphene.NonNull(graphene.String)
    state = graphene.Field(graphene.NonNull(ChallengeState))
    team_size = graphene.Int()
    compensation = graphene.String()
    employee = graphene.Field(Employee)
    keywords = graphene.List(graphene.NonNull('api.schema.keyword.schema.Keyword'))
    match_status = graphene.Field('api.schema.match.MatchStatus')
    match_hints = graphene.Field('api.schema.match.MatchHints')
    date_created = graphene.Date()
    date_published = graphene.Date()

    class Meta:
        model = ChallengeModel
        interfaces = (relay.Node, )
        fields = (
            'title',
            'description',
            'team_size',
            'compensation',
            'challenge_type',
            'company',
            'keywords',
            'website',
            'challenge_from_date',
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
    @restrict_challenge_node
    def get_node(cls, info, id):
        return get_object_or_404(ChallengeModel, pk=id)

    def resolve_avatar_url(self, info):
        return getattr(self.avatar(), 'absolute_url', None)

    def resolve_keywords(self: ChallengeModel, info):
        return self.keywords.all()

    def resolve_title(self, info):
        return self.title

    @hyphenate
    def resolve_display_title(self, info):
        return self.title

    def resolve_match_status(self: ChallengeModel, info):
        user = info.context.user

        if not user.is_authenticated:
            return None

        status = MatchStatus.get(user, challenge=self)

        if status is not None:
            return {'confirmed': status.complete, 'initiator': status.initiator}
        return None

    def resolve_match_hints(self: ChallengeModel, info):
        user = info.context.user

        if not user.is_authenticated:
            return None

        if user.type in ProfileType.valid_company_types():
            return None
        if self.company is None:
            return None
        return user.student.get_match_hints(self.company)


class ChallengeConnection(relay.Connection):

    class Meta:
        node = Challenge


class ChallengeQuery(ObjectType):
    challenge = graphene.Field(Challenge,
                               id=graphene.String(required=False, description=_('Id')),
                               slug=graphene.String(required=False, description=_('Slug')))
    challenges = relay.ConnectionField(
        ChallengeConnection,
        text_search=graphene.String(
            required=False, description=_('Full text search on challenge title and description')),
        challenge_type_ids=graphene.List(graphene.String,
                                         required=False,
                                         description=_('List of challenge type ids')),
        keyword_ids=graphene.List(graphene.String,
                                  description=_('List of keyword ids'),
                                  required=False),
        filter_talent_challenges=graphene.Boolean(description=_('Filter challenges from talents'),
                                                  required=False),
        filter_company_challenges=graphene.Boolean(
            description=_('Filter challenges from companies'), required=False),
        filter_university_challenges=graphene.Boolean(
            description=_('Filter challenges from universities'), required=False),
        team_size=graphene.Int(description=_('Team size'), required=False),
        challenge_from_date=graphene.Date(description=_('Challenge from date'), required=False),
        date_published=graphene.Date(description=_('Date published'), required=False))

    @restrict_challenge
    def resolve_challenge(self, info, **kwargs):
        slug = kwargs.get('slug')
        challenge_id = resolve_node_id(kwargs.get('id'))

        if slug is None and challenge_id is None:
            raise Http404(_('Challenge not found'))

        if slug is not None:
            challenge = get_object_or_404(ChallengeModel, slug=slug)
        elif challenge_id is not None:
            challenge = get_object_or_404(ChallengeModel, pk=challenge_id)

        user = info.context.user

        if user.is_authenticated:
            if user.type in ProfileType.valid_company_types():
                # do not show challenges company <-> company
                if challenge.is_company() and user.company_id != challenge.company_id:
                    raise Http404(_('Challenge not found'))

                # do not show draft challenges of students
                if challenge.is_student() and challenge.state != ChallengeState.PUBLIC:
                    raise Http404(_('Challenge not found'))

            if user.type in ProfileType.valid_student_types():
                # do not show challenges student <-> student
                if challenge.is_student() and user.student.id != challenge.student_id:
                    raise Http404(_('Challenge not found'))

                # do not show draft challenges of companies
                if challenge.is_company() and challenge.state != ChallengeState.PUBLIC:
                    raise Http404(_('Challenge not found'))

        else:
            # hide incomplete challenges from anonymous
            if challenge.state != ChallengeState.PUBLIC:
                raise Http404(_('Challenge not found'))

        return challenge

    @restrict_challenge
    def resolve_challenges(self, info, **kwargs):
        results = search_challenge(info.context.user, kwargs)
        challenge_ids = list(map(lambda hit: hit.get('_id'), results.get('hits').get('hits')))

        return ChallengeModel.objects.filter(id__in=challenge_ids)


class ChallengeBaseData(Output, relay.ClientIDMutation):
    slug = graphene.String()
    challenge_id = graphene.String()

    class Input:
        id = graphene.String(required=False)
        title = graphene.String(description=_('Title'), required=True)
        challenge_type = graphene.Field(ChallengeTypeInput, required=True)
        keywords = graphene.List(KeywordInput, required=True)
        description = graphene.String(description=_('Description'), required=True)
        team_size = graphene.Int(description=_('Team size'), min_value=1, required=True)
        compensation = graphene.String(description=_('Compensation'), required=True)

    class Meta:
        description = _('Creates a challenge')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = resolve_node_ids(data.get('input', None))
        form_data['keywords'] = extract_ids(form_data.get('keywords', []), 'id')

        try:
            challenge = process_challenge_base_data_form(user, form_data)
        except FormException as exception:
            return ChallengeBaseData(success=False, errors=exception.errors)
        return ChallengeBaseData(success=True,
                                 errors=None,
                                 slug=challenge.slug,
                                 challenge_id=to_global_id('Challenge', challenge.id))


class ChallengeSpecificData(Output, relay.ClientIDMutation):
    slug = graphene.String()
    challenge_id = graphene.String()

    class Input:
        id = graphene.String(required=False)
        challenge_from_date = graphene.String(required=False)
        website = graphene.String(required=False)

    class Meta:
        description = _('Creates a challenge')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = resolve_node_ids(data.get('input', None))

        try:
            challenge = process_challenge_specific_data_form(user, form_data)
        except FormException as exception:
            return ChallengeSpecificData(success=False, errors=exception.errors)
        return ChallengeSpecificData(success=True,
                                     errors=None,
                                     slug=challenge.slug,
                                     challenge_id=to_global_id('Challenge', challenge.id))


class ChallengeAllocation(Output, relay.ClientIDMutation):
    slug = graphene.String()
    challenge_id = graphene.String()

    class Input:
        id = graphene.String()
        state = graphene.String(description=_('State'), required=True)
        employee = graphene.Field(EmployeeInput, required=False)

    class Meta:
        description = _('Updates a challenge')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = resolve_node_ids(data.get('input', None))

        try:
            challenge = process_challenge_allocation_form(user, form_data)
        except FormException as exception:
            return ChallengeAllocation(success=False, errors=exception.errors)
        return ChallengeAllocation(success=True,
                                   errors=None,
                                   slug=challenge.slug,
                                   challenge_id=to_global_id('Challenge', challenge.id))


class ChallengeMutation(ObjectType):
    challenge_base_data = ChallengeBaseData.Field()
    challenge_specific_data = ChallengeSpecificData.Field()
    challenge_allocation = ChallengeAllocation.Field()
