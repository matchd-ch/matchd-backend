import graphene
from django.http import Http404
from django.shortcuts import get_object_or_404
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from django.utils.translation import gettext as _
from graphql import ResolveInfo
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

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
from db.forms import process_company_form_step_2, process_company_form_step_3, process_university_form_step_1, \
    process_university_form_step_2, process_university_form_step_3
from db.forms.company_step_1 import process_company_form_step_1
from db.forms.company_step_4 import process_company_form_step_4
from db.forms.university_step_4 import process_university_form_step_4
from db.models import Company as CompanyModel, ProfileState as ProfileStateModel, JobPostingState, ProjectPostingState


class CompanyInput(graphene.InputObjectType):
    id = graphene.ID(required=True)


class RegisterCompanyInput(graphene.InputObjectType):
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
        step1 = CompanyProfileInputStep1(description=_('Profile Input Step 1 is required.'),
                                         required=True)

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
    description = graphene.String(description=_('description'), required=False)
    services = graphene.String(description=_('services'), required=False)
    member_it_st_gallen = graphene.Boolean(description=_('memeber IT St. Gallen'), required=True)


class CompanyProfileStep2(Output, graphene.Mutation):

    class Arguments:
        step2 = CompanyProfileInputStep2(description=_('Profile Input Step 2 is required.'),
                                         required=True)

    class Meta:
        description = _('Updates website url, description, services, member IT St.Gallen')

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
    branches = graphene.List(BranchInput, description=_('Branches'))
    benefits = graphene.List(BenefitInput, description=_('Benefits'))


class CompanyProfileStep3(Output, graphene.Mutation):

    class Arguments:
        step3 = CompanyProfileInputStep3(description=_('Profile Input Step 3 is required.'),
                                         required=True)

    class Meta:
        description = _('Updates the Company Profile with benefits and branches')

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
    soft_skills = graphene.List(SoftSkillInput, description=_('Soft Skills'))
    cultural_fits = graphene.List(CulturalFitInput, description=_('Cultural Fit'))


class CompanyProfileStep4(Output, graphene.Mutation):

    class Arguments:
        step4 = CompanyProfileInputStep4(description=_('Profile Input Step 4 is required.'),
                                         required=True)

    class Meta:
        description = _('Updates a company profile with soft skills and cultural fit')

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
    top_level_organisation_description = graphene.String(description=_('description'),
                                                         required=False)
    top_level_organisation_website = graphene.String(description=_('website dachorganisation'),
                                                     required=False)


class UniversityProfileStep1(Output, graphene.Mutation):

    class Arguments:
        step1 = UniversityProfileInputStep1(description=_('Profile Input Step 1 is required.'),
                                            required=True)

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
    description = graphene.String(description=_('description'), required=False)


class UniversityProfileStep2(Output, graphene.Mutation):

    class Arguments:
        step2 = UniversityProfileInputStep2(description=_('Profile Input Step 2 is required.'),
                                            required=True)

    class Meta:
        description = _('Updates branches and description')

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
    branches = graphene.List(BranchInput, description=_('Branches'))
    benefits = graphene.List(BenefitInput, description=_('Benefits'))


class UniversityProfileStep3(Output, graphene.Mutation):

    class Arguments:
        step3 = UniversityProfileInputStep3(description=_('Profile Input Step 3 is required.'),
                                            required=True)

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


class UniversityProfileInputStep4(graphene.InputObjectType):
    soft_skills = graphene.List(SoftSkillInput, description=_('Soft Skills'))
    cultural_fits = graphene.List(CulturalFitInput, description=_('Cultural Fit'))


class UniversityProfileStep4(Output, graphene.Mutation):

    class Arguments:
        step4 = UniversityProfileInputStep4(description=_('Profile Input Step 4 is required.'),
                                            required=True)

    class Meta:
        description = _('Updates a company profile with soft skills and cultural fit')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('step4', None)
        try:
            process_university_form_step_4(user, form_data)
        except FormException as exception:
            return UniversityProfileStep4(success=False, errors=exception.errors)
        return UniversityProfileStep4(success=True, errors=None)


class UniversityProfileMutation(graphene.ObjectType):
    university_profile_step1 = UniversityProfileStep1.Field()
    university_profile_step2 = UniversityProfileStep2.Field()
    university_profile_step3 = UniversityProfileStep3.Field()
    university_profile_step4 = UniversityProfileStep4.Field()


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
            'id', 'uid', 'name', 'zip', 'city', 'street', 'phone', 'description',
            'member_it_st_gallen', 'services', 'website', 'benefits', 'state', 'profile_step',
            'slug', 'top_level_organisation_description', 'top_level_organisation_website', 'type',
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
