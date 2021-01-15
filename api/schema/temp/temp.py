import graphene


# pylint: disable=R0201
class TempQuery(graphene.ObjectType):
    temp = graphene.Field(
        graphene.Boolean
    )

    def resolve_temp(self, info, **kwargs):
        return True
