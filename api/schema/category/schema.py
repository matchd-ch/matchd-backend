import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.models import Category


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class CategoryQuery(ObjectType):
    categories = graphene.List(CategoryType)

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()
