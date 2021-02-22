import graphene
from django.utils.translation import gettext as _
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from db.exceptions import FormException
from db.forms import process_company_form_step_2
from db.forms.company_step_1 import process_company_form_step_1


class CompanyProfileInputStep1(graphene.InputObjectType):
    first_name = graphene.String(description=_('First name'), required=True)
    last_name = graphene.String(description=_('Last name'), required=True)
    uid = graphene.String(description=_('Uid'), required=True)
    street = graphene.String(description=_('Street'), required=True)
    zip = graphene.String(description=_('Zip'), required=True)
    city = graphene.String(description=_('City'), required=True)
    phone = graphene.String(description=_('Phone Number'))
    email = graphene.String(description=_('Email'), required=True)
    position = graphene.String(description=_('Position'), required=True)


class CompanyProfileStep1(Output, graphene.Mutation):

    class Arguments:
        step1 = CompanyProfileInputStep1(description=_('Profile Input Step 1 is required.'), required=True)

    class Meta:
        description = _('Updates the profile of a Company')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('step1', None)
        try:
            process_company_form_step_1(user, form_data)
        except FormException as exception:
            return CompanyProfileStep1(success=False, errors=exception.errors)
        return CompanyProfileStep1(success=True, errors=None)


class CompanyProfileInputStep2(graphene.InputObjectType):
    website = graphene.String(description=_('website'), required=True)
    branch = graphene.String(description=_('branch'), required=False)
    description = graphene.String(description=_('description'), required=False)
    services = graphene.String(description=_('services'), required=False)
    member_it_st_gallen = graphene.String(description=_('memeber IT St. Gallen'), required=True)


class CompanyProfileStep2(Output, graphene.Mutation):

    class Arguments:
        step2 = CompanyProfileInputStep2(description=_('Profile Input Step 2 is required.'), required=True)

    class Meta:
        description = _('Updates website url, branch, description, services, member IT St.Gallen')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('step2', None)
        try:
            process_company_form_step_2(user, form_data)
        except FormException as exception:
            return CompanyProfileStep2(success=False, errors=exception.errors)
        return CompanyProfileStep2(success=True, errors=None)


class CompanyProfileMutation(graphene.ObjectType):
    company_profile_step1 = CompanyProfileStep1.Field()
    company_profile_step2 = CompanyProfileStep2.Field()
