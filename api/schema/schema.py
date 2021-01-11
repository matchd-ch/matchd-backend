import graphene

from api.schema.temp import TempQuery
from api.schema.user_request import UserRequestMutation


# pylint: disable=R0903
class Mutation(UserRequestMutation):
    pass


class Query(TempQuery):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
