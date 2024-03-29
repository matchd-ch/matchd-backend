import graphene

from graphene import relay
from api.schema.benefit import BenefitQuery
from api.schema.branch import BranchQuery
from api.schema.cultural_fit import CulturalFitQuery
from api.schema.dashboard import DashboardQuery
from api.schema.faq_category import FAQCategoryQuery
from api.schema.company import CompanyProfileMutation, CompanyQuery, UniversityProfileMutation, CompanyMutation
from api.schema.attachment import AttachmentMutation, AttachmentQuery
from api.schema.employee import EmployeeMutation
from api.schema.job_requirement import JobRequirementQuery
from api.schema.job_type import JobTypeQuery
from api.schema.job_posting import JobPostingMutation, JobPostingQuery
from api.schema.keyword.schema import KeywordQuery
from api.schema.language import LanguageQuery
from api.schema.auth import AuthMutation, LogoutMutation, VerifyPasswordResetToken
from api.schema.language_level import LanguageLevelQuery
from api.schema.match import MatchQuery, MatchMutation
from api.schema.challenge.schema import ChallengeQuery, ChallengeMutation
from api.schema.challenge_type.schema import ChallengeTypeQuery
from api.schema.skill import SkillQuery
from api.schema.soft_skill import SoftSkillQuery
from api.schema.student import StudentProfileMutation, StudentQuery, StudentMutation
from api.schema.registration import RegistrationMutation
from api.schema.upload import UploadMutation
from api.schema.upload.schema import UploadConfigurationQuery
from api.schema.user import UserQuery, UserMutation
from api.schema.user_request import UserRequestMutation
from api.schema.zip_city import ZipCityQuery


class Mutation(RegistrationMutation, UserRequestMutation, AuthMutation, LogoutMutation,
               StudentProfileMutation, CompanyProfileMutation, UniversityProfileMutation,
               UploadMutation, AttachmentMutation, JobPostingMutation, EmployeeMutation,
               MatchMutation, ChallengeMutation, UserMutation, StudentMutation, CompanyMutation):
    pass


class Query(VerifyPasswordResetToken, UserQuery, LanguageQuery, LanguageLevelQuery, ZipCityQuery,
            JobTypeQuery, SkillQuery, BenefitQuery, BranchQuery, AttachmentQuery,
            UploadConfigurationQuery, CompanyQuery, JobPostingQuery, JobRequirementQuery,
            FAQCategoryQuery, SoftSkillQuery, CulturalFitQuery, MatchQuery, StudentQuery,
            DashboardQuery, KeywordQuery, ChallengeTypeQuery, ChallengeQuery):
    node = relay.Node.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
