import graphene

from api.schema.benefit import BenefitQuery
from api.schema.branch import BranchQuery
from api.schema.faq_category import FAQCategoryQuery
from api.schema.company import CompanyProfileMutation, CompanyQuery, UniversityProfileMutation
from api.schema.attachment import AttachmentMutation, AttachmentQuery
from api.schema.employee import EmployeeMutation
from api.schema.job_requirement import JobRequirementQuery
from api.schema.job_type import JobTypeQuery
from api.schema.job_position import JobPositionQuery
from api.schema.job_posting import JobPostingMutation, JobPostingQuery
from api.schema.language import LanguageQuery
from api.schema.auth import AuthMutation, LogoutMutation, VerifyPasswordResetToken
from api.schema.language_level import LanguageLevelQuery
from api.schema.skill import SkillQuery
from api.schema.soft_skill import SoftSkillQuery
from api.schema.student import StudentProfileMutation
from api.schema.registration import RegistrationMutation
from api.schema.upload import UploadMutation
from api.schema.upload.schema import UploadConfigurationQuery
from api.schema.user import UserQuery
from api.schema.user_request import UserRequestMutation
from api.schema.zip_city import ZipCityQuery


class Mutation(
    RegistrationMutation,
    UserRequestMutation,
    AuthMutation,
    LogoutMutation,
    StudentProfileMutation,
    CompanyProfileMutation,
    UniversityProfileMutation,
    UploadMutation,
    AttachmentMutation,
    JobPostingMutation,
    EmployeeMutation
):
    pass


class Query(
    VerifyPasswordResetToken,
    UserQuery,
    LanguageQuery,
    LanguageLevelQuery,
    ZipCityQuery,
    JobTypeQuery,
    JobPositionQuery,
    SkillQuery,
    BenefitQuery,
    BranchQuery,
    AttachmentQuery,
    UploadConfigurationQuery,
    CompanyQuery,
    JobPostingQuery,
    JobRequirementQuery,
    FAQCategoryQuery,
    SoftSkillQuery
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
