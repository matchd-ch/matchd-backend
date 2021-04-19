import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_auth.settings import graphql_auth_settings
from graphql_jwt.decorators import login_required

from api.schema.match.schema import MatchHistory
from api.schema.profile_type import ProfileType
from db.models import Match as MatchModel, ProfileType as ProfileTypeModel


class User(DjangoObjectType):
    type = graphene.Field(graphene.NonNull(ProfileType))
    match_history = graphene.Field(graphene.NonNull(MatchHistory))

    class Meta:
        model = get_user_model()
        filter_fields = graphql_auth_settings.USER_NODE_FILTER_FIELDS
        exclude = graphql_auth_settings.USER_NODE_EXCLUDE_FIELDS
        skip_registry = True
        convert_choices_to_enum = False

    def resolve_match_history(self, info):
        user = info.context.user
        has_requested_match = False
        has_confirmed_match = False
        if user.type in ProfileTypeModel.valid_company_types():
            has_requested_match = MatchModel.objects.filter(initiator=user.type, job_posting__employee=user.employee)
            has_confirmed_match = MatchModel.objects.filter(initiator=ProfileTypeModel.STUDENT,
                                                            job_posting__employee=user.employee, company_confirmed=True)
        if user.type in ProfileTypeModel.valid_student_types():
            has_requested_match = MatchModel.objects.filter(initiator=user.type, student=user.student)
            has_confirmed_match = MatchModel.objects.filter(initiator=ProfileTypeModel.COMPANY, student=user.student,
                                                            student_confirmed=True)
        return {
            'has_confirmed_match': has_confirmed_match,
            'has_requested_match': has_requested_match
        }


class UserQuery(graphene.ObjectType):
    me = graphene.Field(User)

    @login_required
    def resolve_me(self, info):
        user = info.context.user
        if user.is_authenticated:
            user = get_user_model().objects.prefetch_related('student', 'company__users',
                                                             'company__benefits', 'company__branches').\
                select_related('company').get(pk=user.id)
            return user
        return None
