import graphene

from api.schema.user_request import UserRequestMutation


# pylint: disable=R0903
class Mutation(UserRequestMutation):
    pass


schema = graphene.Schema(mutation=Mutation)
