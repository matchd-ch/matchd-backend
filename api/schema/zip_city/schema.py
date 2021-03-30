import graphene
from graphene import ObjectType

from api.data import zip_city_datasource


class ZipCity(ObjectType):
    zip = graphene.NonNull(graphene.String)
    city = graphene.NonNull(graphene.String)
    canton = graphene.NonNull(graphene.String)


class ZipCityQuery(ObjectType):
    zip_city = graphene.NonNull(graphene.List(graphene.NonNull(ZipCity)))

    def resolve_zip_city(self, info, **kwargs):
        return zip_city_datasource.data
