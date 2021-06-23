import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Keyword as KeywordModel


class Keyword(DjangoObjectType):

    class Meta:
        model = KeywordModel
        fields = ('id', 'name', )
        convert_choices_to_enum = False


class KeywordQuery(ObjectType):
    keywords = graphene.List(Keyword)

    def resolve_keywords(self, info, **kwargs):
        return KeywordModel.objects.all()


class KeywordInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
