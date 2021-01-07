import graphene

from api.schema.user_request import UserRequestMutation


class Mutation(UserRequestMutation):
    pass


schema = graphene.Schema(mutation=Mutation)
