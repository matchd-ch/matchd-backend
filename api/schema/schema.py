import graphene

from api.schema.job_option import JobOptionQuery
from api.schema.job_position import JobPositionQuery
from api.schema.language import LanguageQuery
from api.schema.auth import AuthMutation, LogoutMutation, VerifyPasswordResetToken
from api.schema.language_level import LanguageLevelQuery
from api.schema.skill import SkillQuery
from api.schema.student import StudentProfileMutation
from api.schema.registration import RegistrationMutation
from api.schema.user import UserQuery
from api.schema.user_request import UserRequestMutation
from api.schema.zip_city import ZipCityQuery


class Mutation(
    RegistrationMutation,
    UserRequestMutation,
    AuthMutation,
    LogoutMutation,
    StudentProfileMutation
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
    SkillQuery
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
