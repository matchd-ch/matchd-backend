import graphene

from db.models import ProfileType as ProfileTypeModel

ProfileType = graphene.Enum.from_enum(ProfileTypeModel)
