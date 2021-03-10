import graphene
from graphene import ObjectType


class EmployeeType(ObjectType):
    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    role = graphene.String()
