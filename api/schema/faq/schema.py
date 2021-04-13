import graphene
from django.shortcuts import get_object_or_404
from graphene import ObjectType
from graphene_django import DjangoObjectType
from django.utils.translation import gettext as _
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from api.schema.faq_category.schema import FAQCategory, FAQCategoryInput
from db.exceptions import FormException
from db.forms.faq import process_add_faq, process_update_faq
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


class AddFAQInput(graphene.InputObjectType):
    category = graphene.Field(FAQCategoryInput, description=_('category'), required=True)
    title = graphene.String(description=_('title'), required=True)
    question = graphene.String(description=_('question'), required=True)
    answer = graphene.String(description=_('answer'), required=True)


class AddFAQ(Output, graphene.Mutation):
    class Arguments:
        add_faq = AddFAQInput(description=_('FAQ input is required'), required=True)

    class Meta:
        description = _('add FAQ to your company')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('add_faq', None)
        try:
            process_add_faq(user, form_data)
        except FormException as exception:
            return AddFAQ(success=False, errors=exception.errors)
        return AddFAQ(success=True, errors=None)


class UpdateFAQInput(graphene.InputObjectType):
    faq_id = graphene.ID(description=_('Faq ID'), required=True)
    category = graphene.Field(FAQCategoryInput, description=_('category'), required=True)
    title = graphene.String(description=_('title'), required=True)
    question = graphene.String(description=_('question'), required=True)
    answer = graphene.String(description=_('answer'), required=True)


class UpdateFAQ(Output, graphene.Mutation):
    class Arguments:
        update_faq = UpdateFAQInput(description=_('FAQ input is required'), required=True)

    class Meta:
        description = _('updates FAQ from your company')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('update_faq', None)
        try:
            process_update_faq(user, form_data)
        except FormException as exception:
            return UpdateFAQ(success=False, errors=exception.errors)
        return UpdateFAQ(success=True, errors=None)


class FAQMutation(graphene.ObjectType):
    add_faq = AddFAQ.Field()
    update_faq = UpdateFAQ.Field()
