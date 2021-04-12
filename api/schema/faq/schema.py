import graphene
from django.shortcuts import get_object_or_404
from graphene import ObjectType
from graphene_django import DjangoObjectType

from api.schema.faq_category.schema import FAQCategory
from db.models import FAQ as FAQmodel, Company, FAQCategory as FAQCategoryModel


class FAQ(DjangoObjectType):
    class Meta:
        model = FAQmodel
        fields = ('id', 'category', 'title', 'question', 'answer',)


class FAQQuery(ObjectType):
    company_faqs = graphene.List(FAQCategory, slug=graphene.String())

    def resolve_company_faqs(self, info, slug):
        company_id = get_object_or_404(Company, slug=slug).id
        faq_categories = FAQCategoryModel.objects.filter(faqs__company__id=company_id).distinct()
        return faq_categories


class FAQInput(graphene.InputObjectType):
    category = graphene.ID(required=True)
    title = graphene.String(required=False)
    question = graphene.String(required=False)
    answer = graphene.String(required=False)
