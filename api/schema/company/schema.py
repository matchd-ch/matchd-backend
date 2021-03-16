import graphene
from django.http import Http404
from django.shortcuts import get_object_or_404
from graphene import ObjectType
from graphene_django import DjangoObjectType
from django.utils.translation import gettext as _
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from api.schema.benefit import BenefitInputType
from api.schema.branch.schema import BranchInputType
from api.schema.job_position import JobPositionInputType
from api.schema.user.schema import Employee
from db.exceptions import FormException
from db.forms import process_company_form_step_2, process_company_form_step_3
from db.forms.company_step_1 import process_company_form_step_1
from db.models import Company as CompanyModel, Employee as EmployeeModel, UserState


class CompanyProfileInputStep1(graphene.InputObjectType):
    first_name = graphene.String(description=_('First name'), required=True)
    last_name = graphene.String(description=_('Last name'), required=True)
    name = graphene.String(description=_('Name'), required=False)
    street = graphene.String(description=_('Street'), required=True)
    zip = graphene.String(description=_('Zip'), required=True)
    city = graphene.String(description=_('City'), required=True)
    phone = graphene.String(description=_('Phone Number'))
    role = graphene.String(description=_('role'), required=True)


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
    branch = graphene.Field(BranchInputType, description=_('branch'), required=False)
    description = graphene.String(description=_('description'), required=False)
    services = graphene.String(description=_('services'), required=False)
    member_it_st_gallen = graphene.Boolean(description=_('memeber IT St. Gallen'), required=True)


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


class CompanyProfileInputStep3(graphene.InputObjectType):
    job_positions = graphene.List(JobPositionInputType, description=_('Job Position'))
    benefits = graphene.List(BenefitInputType, description=_('Benefits'))


class CompanyProfileStep3(Output, graphene.Mutation):
    class Arguments:
        step3 = CompanyProfileInputStep3(description=_('Profile Input Step 3 is required.'), required=True)

    class Meta:
        description = _('Updates the Company Profile with benefits and Job Positions')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('step3', None)
        try:
            process_company_form_step_3(user, form_data)
        except FormException as exception:
            return CompanyProfileStep3(success=False, errors=exception.errors)
        return CompanyProfileStep3(success=True, errors=None)


class CompanyProfileMutation(graphene.ObjectType):
    company_profile_step1 = CompanyProfileStep1.Field()
    company_profile_step2 = CompanyProfileStep2.Field()
    company_profile_step3 = CompanyProfileStep3.Field()


class Company(DjangoObjectType):
    employees = graphene.List(Employee)

    class Meta:
        model = CompanyModel
        fields = ['uid', 'name', 'zip', 'city', 'street', 'phone', 'description', 'member_it_st_gallen',
                  'services', 'website', 'job_positions', 'benefits']

    def resolve_employees(self: CompanyModel, info):
        users = self.users.prefetch_related('employee').all()
        employees = []
        for user in users:
            employees.append(user.employee)
        return employees


class CompanyQuery(ObjectType):
    company = graphene.Field(Company, slug=graphene.String())

    def resolve_company(self, info, slug):
        company = get_object_or_404(CompanyModel, slug=slug)
        if len(company.users.all()) >= 1:
            if company.users.all()[0].state == UserState.PUBLIC:
                return company

        raise Http404(_('Company not found'))
