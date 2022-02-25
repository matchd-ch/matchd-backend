import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from db.models import JobPostingLanguageRelation as JobPostingLanguageRelationModel


class JobPostingLanguageRelation(DjangoObjectType):

    class Meta:
        model = JobPostingLanguageRelationModel
        interfaces = (relay.Node, )
        fields = (
            'language',
            'language_level',
        )

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.select_related('language', 'language_level')


class JobPostingLanguageRelationInput(graphene.InputObjectType):
    id = graphene.String()
    language = graphene.String()
    language_level = graphene.String()

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
