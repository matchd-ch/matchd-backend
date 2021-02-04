import graphene

from api.schema.hobby import HobbyQuery
from api.schema.language import LanguageQuery
from api.schema.auth import AuthMutation, LogoutMutation, VerifyPasswordResetToken
from api.schema.language_level import LanguageLevelQuery
from api.schema.profile import StudentProfileMutation
from api.schema.skill import SkillQuery
from api.schema.registration import RegistrationMutation
from api.schema.user import UserQuery
from api.schema.user_request import UserRequestMutation


class Mutation(
    RegistrationMutation,
    UserRequestMutation,
    AuthMutation,
    LogoutMutation,
    StudentProfileMutation
):
    pass


class Query(VerifyPasswordResetToken, UserQuery, SkillQuery, LanguageQuery, LanguageLevelQuery, HobbyQuery):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
