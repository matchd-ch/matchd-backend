import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphql import ResolveInfo
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from api.helper import is_me_query
from api.schema.benefit import BenefitInput
from api.schema.branch.schema import BranchInput
from api.schema.cultural_fit import CulturalFitInput
from api.schema.employee import Employee
from api.schema.soft_skill import SoftSkillInput
from api.schema.profile_state import ProfileState
from api.schema.profile_type import ProfileType

from db.decorators import company_cheating_protection, hyphenate
from db.exceptions import FormException
from db.forms import process_company_relations_form, process_company_advantages_form, \
    process_university_base_data_form, process_university_specific_data_form, process_university_relations_form
from db.forms.company_base_data import process_company_base_data_form
from db.forms.company_values import process_company_values_form
from db.forms.university_values import process_university_values_form
from db.models import Company as CompanyModel, ProfileState as ProfileStateModel, JobPostingState, ProjectPostingState


class CompanyInput(graphene.InputObjectType):
    id = graphene.ID(required=True)


class RegisterCompanyInput(graphene.InputObjectType):
    name = graphene.String(description=_('Name'), required=True)
    uid = graphene.String(description=_('UID'))
    zip = graphene.String(description=_('ZIP'), required=True)
    city = graphene.String(description=_('City'), required=True)


class CompanyProfileInputBaseData(graphene.InputObjectType):
    first_name = graphene.String(description=_('First name'), required=True)
    last_name = graphene.String(description=_('Last name'), required=True)
    name = graphene.String(description=_('Name'), required=False)
    street = graphene.String(description=_('Street'), required=True)
    zip = graphene.String(description=_('Zip'), required=True)
    city = graphene.String(description=_('City'), required=True)
    phone = graphene.String(description=_('Phone Number'))
    role = graphene.String(description=_('role'), required=True)


class CompanyProfileBaseData(Output, graphene.Mutation):

    class Arguments:
        base_data = CompanyProfileInputBaseData(
            description=_('Profile Input Base Data is required.'), required=True)

    class Meta:
        description = _('Updates the profile of a Company')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('base_data', None)
        try:
            process_company_base_data_form(user, form_data)
        except FormException as exception:
            return CompanyProfileBaseData(success=False, errors=exception.errors)
        return CompanyProfileBaseData(success=True, errors=None)


class CompanyProfileInputRelations(graphene.InputObjectType):
    website = graphene.String(description=_('website'), required=True)
    description = graphene.String(description=_('description'), required=False)
    services = graphene.String(description=_('services'), required=False)
    member_it_st_gallen = graphene.Boolean(description=_('memeber IT St. Gallen'), required=True)


class CompanyProfileRelations(Output, graphene.Mutation):

    class Arguments:
        relations = CompanyProfileInputRelations(
            description=_('Profile Input Relations is required.'), required=True)

    class Meta:
        description = _('Updates website url, description, services, member IT St.Gallen')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('relations', None)
        try:
            process_company_relations_form(user, form_data)
        except FormException as exception:
            return CompanyProfileRelations(success=False, errors=exception.errors)
        return CompanyProfileRelations(success=True, errors=None)


class CompanyProfileInputAdvantages(graphene.InputObjectType):
    branches = graphene.List(BranchInput, description=_('Branches'))
    benefits = graphene.List(BenefitInput, description=_('Benefits'))


class CompanyProfileAdvantages(Output, graphene.Mutation):

    class Arguments:
        advantages = CompanyProfileInputAdvantages(
            description=_('Profile Input Advantages is required.'), required=True)

    class Meta:
        description = _('Updates the Company Profile with benefits and branches')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('advantages', None)
        try:
            process_company_advantages_form(user, form_data)
        except FormException as exception:
            return CompanyProfileAdvantages(success=False, errors=exception.errors)
        return CompanyProfileAdvantages(success=True, errors=None)


class CompanyProfileInputValues(graphene.InputObjectType):
    soft_skills = graphene.List(SoftSkillInput, description=_('Soft Skills'))
    cultural_fits = graphene.List(CulturalFitInput, description=_('Cultural Fit'))


class CompanyProfileValues(Output, graphene.Mutation):

    class Arguments:
        values = CompanyProfileInputValues(description=_('Profile Input Values is required.'),
                                           required=True)

    class Meta:
        description = _('Updates a company profile with soft skills and cultural fit')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('values', None)
        try:
            process_company_values_form(user, form_data)
        except FormException as exception:
            return CompanyProfileValues(success=False, errors=exception.errors)
        return CompanyProfileValues(success=True, errors=None)


class CompanyProfileMutation(ObjectType):
    company_profile_base_data = CompanyProfileBaseData.Field()
    company_profile_relations = CompanyProfileRelations.Field()
    company_profile_advantages = CompanyProfileAdvantages.Field()
    company_profile_values = CompanyProfileValues.Field()


class UniversityProfileInputBaseData(graphene.InputObjectType):
    first_name = graphene.String(description=_('First name'), required=True)
    last_name = graphene.String(description=_('Last name'), required=True)
    name = graphene.String(description=_('Name'), required=False)
    street = graphene.String(description=_('Street'), required=True)
    zip = graphene.String(description=_('Zip'), required=True)
    city = graphene.String(description=_('City'), required=True)
    phone = graphene.String(description=_('Phone Number'))
    role = graphene.String(description=_('role'), required=True)
    website = graphene.String(description=_('website'), required=True)
    top_level_organisation_description = graphene.String(description=_('description'),
                                                         required=False)
    top_level_organisation_website = graphene.String(description=_('website dachorganisation'),
                                                     required=False)


class UniversityProfileBaseData(Output, graphene.Mutation):

    class Arguments:
        base_data = UniversityProfileInputBaseData(
            description=_('Profile Input Base Data is required.'), required=True)

    class Meta:
        description = _('Updates the profile of a university')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('base_data', None)
        try:
            process_university_base_data_form(user, form_data)
        except FormException as exception:
            return UniversityProfileBaseData(success=False, errors=exception.errors)
        return UniversityProfileBaseData(success=True, errors=None)


class UniversityProfileInputSpecificData(graphene.InputObjectType):
    description = graphene.String(description=_('description'), required=False)


class UniversityProfileSpecificData(Output, graphene.Mutation):

    class Arguments:
        specific_data = UniversityProfileInputSpecificData(
            description=_('Profile Input Specific Data is required.'), required=True)

    class Meta:
        description = _('Updates branches and description')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('specific_data', None)
        try:
            process_university_specific_data_form(user, form_data)
        except FormException as exception:
            return UniversityProfileSpecificData(success=False, errors=exception.errors)
        return UniversityProfileSpecificData(success=True, errors=None)


class UniversityProfileInputRelations(graphene.InputObjectType):
    services = graphene.String(description=_('services'), required=False)
    link_education = graphene.String(description=_('website education'), required=False)
    link_projects = graphene.String(description=_('website projects'), required=False)
    link_thesis = graphene.String(description=_('website thesis'), required=False)
    branches = graphene.List(BranchInput, description=_('Branches'))
    benefits = graphene.List(BenefitInput, description=_('Benefits'))


class UniversityProfileRelations(Output, graphene.Mutation):

    class Arguments:
        relations = UniversityProfileInputRelations(
            description=_('Profile Input Relations is required.'), required=True)

    class Meta:
        description = _('Updates website services')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('relations', None)
        try:
            process_university_relations_form(user, form_data)
        except FormException as exception:
            return UniversityProfileRelations(success=False, errors=exception.errors)
        return UniversityProfileRelations(success=True, errors=None)


class UniversityProfileInputValues(graphene.InputObjectType):
    soft_skills = graphene.List(SoftSkillInput, description=_('Soft Skills'))
    cultural_fits = graphene.List(CulturalFitInput, description=_('Cultural Fit'))


class UniversityProfileValues(Output, graphene.Mutation):

    class Arguments:
        values = UniversityProfileInputValues(description=_('Profile Input Values is required.'),
                                              required=True)

    class Meta:
        description = _('Updates a company profile with soft skills and cultural fit')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('values', None)
        try:
            process_university_values_form(user, form_data)
        except FormException as exception:
            return UniversityProfileValues(success=False, errors=exception.errors)
        return UniversityProfileValues(success=True, errors=None)


class UniversityProfileMutation(ObjectType):
    university_profile_base_data = UniversityProfileBaseData.Field()
    university_profile_specific_data = UniversityProfileSpecificData.Field()
    university_profile_relations = UniversityProfileRelations.Field()
    university_profile_values = UniversityProfileValues.Field()


class Company(DjangoObjectType):
    employees = graphene.NonNull(graphene.List(graphene.NonNull(Employee)))
    job_postings = graphene.NonNull(
        graphene.List(graphene.NonNull('api.schema.job_posting.schema.JobPosting')))
    project_postings = graphene.NonNull(
        graphene.List(graphene.NonNull('api.schema.project_posting.schema.ProjectPosting')))
    type = graphene.Field(graphene.NonNull(ProfileType))
    state = graphene.Field(graphene.NonNull(ProfileState))
    soft_skills = graphene.List(graphene.NonNull('api.schema.soft_skill.schema.SoftSkill'))
    cultural_fits = graphene.List(graphene.NonNull('api.schema.cultural_fit.schema.CulturalFit'))
    name = graphene.NonNull(graphene.String)
    display_name = graphene.NonNull(graphene.String)

    class Meta:
        model = CompanyModel
        interfaces = (relay.Node, )
        fields = [
            'uid', 'name', 'zip', 'city', 'street', 'phone', 'description', 'member_it_st_gallen',
            'services', 'website', 'benefits', 'state', 'profile_step', 'slug',
            'top_level_organisation_description', 'top_level_organisation_website', 'type',
            'branches', 'link_education', 'link_projects', 'link_thesis', 'soft_skills',
            'cultural_fits', 'job_postings'
        ]
        convert_choices_to_enum = False

    def resolve_employees(self: CompanyModel, info):
        users = self.users.prefetch_related('employee').all()
        employees = []
        for user in users:
            employees.append(user.employee)
        return employees

    def resolve_job_postings(self: CompanyModel, info: ResolveInfo):
        if is_me_query(info):
            return self.job_postings.all()
        return self.job_postings.filter(state=JobPostingState.PUBLIC)

    def resolve_project_postings(self: CompanyModel, info: ResolveInfo):
        if is_me_query(info):
            return self.project_postings.all()
        return self.project_postings.filter(state=ProjectPostingState.PUBLIC)

    @company_cheating_protection
    def resolve_soft_skills(self: CompanyModel, info: ResolveInfo):
        return self.soft_skills.all()

    @company_cheating_protection
    def resolve_cultural_fits(self: CompanyModel, info: ResolveInfo):
        return self.cultural_fits.all()

    def resolve_name(self, info):
        return self.name

    @hyphenate
    def resolve_display_name(self, info):
        return self.name


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
