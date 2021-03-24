import graphene
from django.http import Http404
from django.shortcuts import get_object_or_404
from graphene import ObjectType
from graphene_django import DjangoObjectType
from django.utils.translation import gettext as _
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from api.schema.benefit import BenefitInput
from api.schema.branch.schema import BranchInput
from api.schema.employee import Employee
from api.schema.job_position import JobPositionInput
from api.schema.soft_skill import SoftSkillInputType
from api.schema.profile_state import ProfileState
from api.schema.profile_type import ProfileType
from db.exceptions import FormException
from db.forms import process_company_form_step_2, process_company_form_step_3, process_university_form_step_1, \
    process_university_form_step_2, process_university_form_step_3
from db.forms.company_step_1 import process_company_form_step_1
from db.forms.company_step_4 import process_company_form_step_4
from db.models import Company as CompanyModel, ProfileState as ProfileStateModel


class CompanyInput(graphene.InputObjectType):
    name = graphene.String(description=_('Name'), required=True)
    uid = graphene.String(description=_('UID'))
    zip = graphene.String(description=_('ZIP'), required=True)
    city = graphene.String(description=_('City'), required=True)


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
    branch = graphene.Field(BranchInput, description=_('branch'), required=False)
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
    job_positions = graphene.List(JobPositionInput, description=_('Job Position'))
    benefits = graphene.List(BenefitInput, description=_('Benefits'))


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


class CompanyProfileInputStep4(graphene.InputObjectType):
    soft_skills = graphene.List(SoftSkillInputType, description=_('Soft Skills'))


class CompanyProfileStep4(Output, graphene.Mutation):
    class Arguments:
        step4 = CompanyProfileInputStep4(description=_('Profile Input Step 4 is required.'), required=True)

    class Meta:
        description = _('Updates the Company Profile with Soft Skills')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('step4', None)
        try:
            process_company_form_step_4(user, form_data)
        except FormException as exception:
            return CompanyProfileStep4(success=False, errors=exception.errors)
        return CompanyProfileStep4(success=True, errors=None)


class CompanyProfileMutation(graphene.ObjectType):
    company_profile_step1 = CompanyProfileStep1.Field()
    company_profile_step2 = CompanyProfileStep2.Field()
    company_profile_step3 = CompanyProfileStep3.Field()
    company_profile_step4 = CompanyProfileStep4.Field()


class UniversityProfileInputStep1(graphene.InputObjectType):
    first_name = graphene.String(description=_('First name'), required=True)
    last_name = graphene.String(description=_('Last name'), required=True)
    name = graphene.String(description=_('Name'), required=False)
    street = graphene.String(description=_('Street'), required=True)
    zip = graphene.String(description=_('Zip'), required=True)
    city = graphene.String(description=_('City'), required=True)
    phone = graphene.String(description=_('Phone Number'))
    role = graphene.String(description=_('role'), required=True)
    website = graphene.String(description=_('website'), required=True)
    top_level_organisation_description = graphene.String(description=_('description'), required=False)
    top_level_organisation_website = graphene.String(description=_('website dachorganisation'), required=False)


class UniversityProfileStep1(Output, graphene.Mutation):
    class Arguments:
        step1 = UniversityProfileInputStep1(description=_('Profile Input Step 1 is required.'), required=True)

    class Meta:
        description = _('Updates the profile of a university')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('step1', None)
        try:
            process_university_form_step_1(user, form_data)
        except FormException as exception:
            return UniversityProfileStep1(success=False, errors=exception.errors)
        return UniversityProfileStep1(success=True, errors=None)


class UniversityProfileInputStep2(graphene.InputObjectType):
    branch = graphene.Field(BranchInput, description=_('branch'), required=False)
    description = graphene.String(description=_('description'), required=False)


class UniversityProfileStep2(Output, graphene.Mutation):
    class Arguments:
        step2 = UniversityProfileInputStep2(description=_('Profile Input Step 2 is required.'), required=True)

    class Meta:
        description = _('Updates website branch and description')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('step2', None)
        try:
            process_university_form_step_2(user, form_data)
        except FormException as exception:
            return UniversityProfileStep2(success=False, errors=exception.errors)
        return UniversityProfileStep2(success=True, errors=None)


class UniversityProfileInputStep3(graphene.InputObjectType):
    services = graphene.String(description=_('services'), required=False)
    link_education = graphene.String(description=_('website education'), required=False)
    link_projects = graphene.String(description=_('website projects'), required=False)
    link_thesis = graphene.String(description=_('website thesis'), required=False)


class UniversityProfileStep3(Output, graphene.Mutation):
    class Arguments:
        step3 = UniversityProfileInputStep3(description=_('Profile Input Step 3 is required.'), required=True)

    class Meta:
        description = _('Updates website services')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('step3', None)
        try:
            process_university_form_step_3(user, form_data)
        except FormException as exception:
            return UniversityProfileStep3(success=False, errors=exception.errors)
        return UniversityProfileStep3(success=True, errors=None)


class UniversityProfileMutation(graphene.ObjectType):
    university_profile_step1 = UniversityProfileStep1.Field()
    university_profile_step2 = UniversityProfileStep2.Field()
    university_profile_step3 = UniversityProfileStep3.Field()


class Company(DjangoObjectType):
    employees = graphene.NonNull(graphene.List(graphene.NonNull(Employee)))
    type = graphene.Field(graphene.NonNull(ProfileType))
    state = graphene.Field(graphene.NonNull(ProfileState))

    class Meta:
        model = CompanyModel
        fields = ['id', 'uid', 'name', 'zip', 'city', 'street', 'phone', 'description', 'member_it_st_gallen',
                  'services', 'website', 'job_positions', 'benefits', 'state', 'profile_step', 'slug',
                  'top_level_organisation_description', 'top_level_organisation_website', 'type', 'branch',
                  'link_education', 'link_projects', 'link_thesis', 'soft_skills']
        convert_choices_to_enum = False

    def resolve_employees(self: CompanyModel, info):
        users = self.users.prefetch_related('employee').all()
        employees = []
        for user in users:
            employees.append(user.employee)
        return employees


class CompanyQuery(ObjectType):
    company = graphene.Field(Company, slug=graphene.String())

    def resolve_company(self, info, slug):
        user = info.context.user

        company = get_object_or_404(CompanyModel, slug=slug)
        employee_users = company.users.all()

        # check if the state is public or the user is an employee of the company
        if user in employee_users or company.state == ProfileStateModel.PUBLIC:
            return company

        raise Http404(_('Company not found'))
