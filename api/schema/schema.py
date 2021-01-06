import graphene

from api.schema.user_request import UserRequestMutation


schema = graphene.Schema()


class Mutation(UserRequestMutation):
    pass


schema = graphene.Schema(mutation=Mutation)
