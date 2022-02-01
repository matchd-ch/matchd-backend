import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from db.models import Keyword as KeywordModel


class Keyword(DjangoObjectType):

    class Meta:
        model = KeywordModel
        interfaces = (relay.Node,)
        fields = ('name', )
        convert_choices_to_enum = False


class KeywordConnection(relay.Connection):

    class Meta:
        node = Keyword


class KeywordQuery(ObjectType):
    keywords = relay.ConnectionField(KeywordConnection)

    def resolve_keywords(self, info, **kwargs):
        return KeywordModel.objects.all()


class KeywordInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=False)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
