import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphql.type import GraphQLResolveInfo
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from api.helper import extract_ids, is_me_query, resolve_node_id, resolve_node_ids
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
    process_university_base_data_form, process_university_specific_data_form, process_university_relations_form, \
    update_company_info
from db.forms.company_base_data import process_company_base_data_form
from db.forms.company_values import process_company_values_form
from db.forms.university_values import process_university_values_form
from db.models import Company as CompanyModel, ProfileState as ProfileStateModel, JobPostingState, ChallengeState

# pylint: disable=W0221


class CompanyInput(graphene.InputObjectType):
    id = graphene.String(required=True)


class RegisterCompanyInput(graphene.InputObjectType):
    name = graphene.String(description=_('Name'), required=True)
    uid = graphene.String(description=_('UID'))
    zip = graphene.String(description=_('ZIP'), required=True)
    city = graphene.String(description=_('City'), required=True)


class CompanyProfileBaseData(Output, relay.ClientIDMutation):

    class Input:
        first_name = graphene.String(description=_('First name'), required=True)
        last_name = graphene.String(description=_('Last name'), required=True)
        name = graphene.String(description=_('Name'), required=False)
        street = graphene.String(description=_('Street'), required=True)
        zip = graphene.String(description=_('Zip'), required=True)
        city = graphene.String(description=_('City'), required=True)
        phone = graphene.String(description=_('Phone Number'))
        role = graphene.String(description=_('role'), required=True)

    class Meta:
        description = _('Updates the profile of a Company')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('input', None)
        try:
            process_company_base_data_form(user, form_data)
        except FormException as exception:
            return CompanyProfileBaseData(success=False, errors=exception.errors)
        return CompanyProfileBaseData(success=True, errors=None)


class CompanyProfileRelations(Output, relay.ClientIDMutation):

    class Input:
        website = graphene.String(description=_('website'), required=True)
        description = graphene.String(description=_('description'), required=False)
        services = graphene.String(description=_('services'), required=False)
        member_it_st_gallen = graphene.Boolean(description=_('memeber IT St. Gallen'),
                                               required=True)

    class Meta:
        description = _('Updates website url, description, services, member IT St.Gallen')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('input', None)

        try:
            process_company_relations_form(user, form_data)
        except FormException as exception:
            return CompanyProfileRelations(success=False, errors=exception.errors)
        return CompanyProfileRelations(success=True, errors=None)


class CompanyProfileAdvantages(Output, relay.ClientIDMutation):

    class Input:
        branches = graphene.List(BranchInput, description=_('Branches'))
        benefits = graphene.List(BenefitInput, description=_('Benefits'))

    class Meta:
        description = _('Updates the Company Profile with benefits and branches')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = resolve_node_ids(data.get('input', None))
        form_data['branches'] = extract_ids(form_data.get('branches', []), 'id')
        form_data['benefits'] = extract_ids(form_data.get('benefits', []), 'id')

        try:
            process_company_advantages_form(user, form_data)
        except FormException as exception:
            return CompanyProfileAdvantages(success=False, errors=exception.errors)
        return CompanyProfileAdvantages(success=True, errors=None)


class CompanyProfileValues(Output, relay.ClientIDMutation):

    class Input:
        soft_skills = graphene.List(SoftSkillInput, description=_('Soft Skills'))
        cultural_fits = graphene.List(CulturalFitInput, description=_('Cultural Fit'))

    class Meta:
        description = _('Updates a company profile with soft skills and cultural fit')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = resolve_node_ids(data.get('input', None))
        form_data['soft_skills'] = extract_ids(form_data.get('soft_skills', []), 'id')
        form_data['cultural_fits'] = extract_ids(form_data.get('cultural_fits', []), 'id')

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


class UniversityProfileBaseData(Output, relay.ClientIDMutation):

    class Input:
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

    class Meta:
        description = _('Updates the profile of a university')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('input', None)

        try:
            process_university_base_data_form(user, form_data)
        except FormException as exception:
            return UniversityProfileBaseData(success=False, errors=exception.errors)
        return UniversityProfileBaseData(success=True, errors=None)


class UniversityProfileSpecificData(Output, relay.ClientIDMutation):

    class Input:
        description = graphene.String(description=_('description'), required=False)

    class Meta:
        description = _('Updates branches and description')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('input', None)

        try:
            process_university_specific_data_form(user, form_data)
        except FormException as exception:
            return UniversityProfileSpecificData(success=False, errors=exception.errors)
        return UniversityProfileSpecificData(success=True, errors=None)


class UniversityProfileRelations(Output, relay.ClientIDMutation):

    class Input:
        services = graphene.String(description=_('services'), required=False)
        link_education = graphene.String(description=_('website education'), required=False)
        link_challenges = graphene.String(description=_('website challenges'), required=False)
        link_thesis = graphene.String(description=_('website thesis'), required=False)
        branches = graphene.List(BranchInput, description=_('Branches'))
        benefits = graphene.List(BenefitInput, description=_('Benefits'))

    class Meta:
        description = _('Updates website services')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = resolve_node_ids(data.get('input', None))
        form_data['branches'] = extract_ids(form_data.get('branches', []), 'id')
        form_data['benefits'] = extract_ids(form_data.get('benefits', []), 'id')

        try:
            process_university_relations_form(user, form_data)
        except FormException as exception:
            return UniversityProfileRelations(success=False, errors=exception.errors)
        return UniversityProfileRelations(success=True, errors=None)


class UniversityProfileValues(Output, relay.ClientIDMutation):

    class Input:
        soft_skills = graphene.List(SoftSkillInput, description=_('Soft Skills'))
        cultural_fits = graphene.List(CulturalFitInput, description=_('Cultural Fit'))

    class Meta:
        description = _('Updates a company profile with soft skills and cultural fit')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = resolve_node_ids(data.get('input', None))
        form_data['soft_skills'] = extract_ids(form_data.get('soft_skills', []), 'id')
        form_data['cultural_fits'] = extract_ids(form_data.get('cultural_fits', []), 'id')

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
    challenges = graphene.NonNull(
        graphene.List(graphene.NonNull('api.schema.challenge.schema.Challenge')))
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
            'branches', 'link_education', 'link_challenges', 'link_thesis', 'soft_skills',
            'cultural_fits', 'job_postings'
        ]
        convert_choices_to_enum = False

    def resolve_employees(self: CompanyModel, info):
        return self.get_employees()

    def resolve_job_postings(self: CompanyModel, info: GraphQLResolveInfo):
        if is_me_query(info):
            return self.job_postings.all()
        return self.job_postings.filter(state=JobPostingState.PUBLIC)

    def resolve_challenges(self: CompanyModel, info: GraphQLResolveInfo):
        if is_me_query(info):
            return self.challenges.all()
        return self.challenges.filter(state=ChallengeState.PUBLIC)

    @company_cheating_protection
    def resolve_soft_skills(self: CompanyModel, info: GraphQLResolveInfo):
        return self.soft_skills.all()

    @company_cheating_protection
    def resolve_cultural_fits(self: CompanyModel, info: GraphQLResolveInfo):
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


class UpdateCompanyMutation(Output, relay.ClientIDMutation):
    company = graphene.Field(Company)

    class Input:
        id = graphene.String(required=True)
        name = graphene.String(required=False)
        state = graphene.Field(ProfileState)

    class Meta:
        description = _('Updates company information')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user

        company_data = data.get('input', None)
        company_id = resolve_node_id(company_data.get('id'))

        company = CompanyModel.objects.get(pk=company_id)

        if not company.users.filter(pk=user.id).exists():
            return UpdateCompanyMutation(success=False,
                                         errors=_('The user is not part of the company'),
                                         company=None)

        try:
            updated_company = update_company_info(company, company_data)
        except FormException as exception:
            return UpdateCompanyMutation(success=False, errors=exception.errors, company=None)
        return UpdateCompanyMutation(success=True, errors=None, company=updated_company)


class CompanyMutation(graphene.ObjectType):
    update_company = UpdateCompanyMutation.Field()
