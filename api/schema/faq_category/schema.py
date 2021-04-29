import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from api.helper import is_faq_categories_query, retrieve_param_from_info
from db.models import FAQCategory as FAQCategoryModel


class FAQCategory(DjangoObjectType):
    faqs = graphene.List('api.schema.faq.FAQ')

    class Meta:
        model = FAQCategoryModel
        fields = ('id', 'name', 'faqs',)

    def resolve_faqs(self, info, **kwargs):
        if is_faq_categories_query(info):
            return None
        slug = retrieve_param_from_info(info, 'slug', 0)

        return self.faqs.filter(company__slug=slug)


class FAQCategoryQuery(ObjectType):
    faq_categories = graphene.List(FAQCategory)

    def resolve_faq_categories(self, info, **kwargs):
        return FAQCategoryModel.objects.all()


class FAQCategoryInput(graphene.InputObjectType):
    id = graphene.ID(required=True)

    # pylint: disable=C0103
    @property
    def pk(self):
        return self.id
