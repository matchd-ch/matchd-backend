import graphene


# pylint: disable=R0903
from api.schema.auth import AuthMutation, VerifyPasswordResetToken
from api.schema.registration import RegistrationMutation
from api.schema.user_request import UserRequestMutation


# pylint: disable=R0903
class Mutation(
    RegistrationMutation,
    UserRequestMutation,
    AuthMutation,

):
    pass


class Query(VerifyPasswordResetToken):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
