import graphene

from db.models import ProfileState as ProfileStateModel

ProfileState = graphene.Enum.from_enum(ProfileStateModel)
