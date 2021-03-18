import graphene

from api.schema.benefit import BenefitQuery
from api.schema.branch import BranchQuery
from api.schema.company import CompanyProfileMutation, CompanyQuery
from api.schema.attachment import AttachmentMutation, AttachmentQuery
from api.schema.expectation import ExpectationQuery
from api.schema.job_option import JobOptionQuery
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
    UploadMutation,
    AttachmentMutation,
    JobPostingMutation
):
    pass


class Query(
    VerifyPasswordResetToken,
    UserQuery,
    LanguageQuery,
    LanguageLevelQuery,
    ZipCityQuery,
    JobOptionQuery,
    JobPositionQuery,
    SkillQuery,
    BenefitQuery,
    BranchQuery,
    AttachmentQuery,
    UploadConfigurationQuery,
    CompanyQuery,
    JobPostingQuery,
    ExpectationQuery,
    SoftSkillQuery
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
