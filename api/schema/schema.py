import graphene


# pylint: disable=R0903
from api.schema.auth import AuthMutation
from api.schema.registration import RegistrationMutation
from api.schema.user_request import UserRequestMutation
from api.schema.temp import TempQuery


# pylint: disable=R0903
class Mutation(
    RegistrationMutation,
    UserRequestMutation,
    AuthMutation,

):
    pass


class Query(TempQuery):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
