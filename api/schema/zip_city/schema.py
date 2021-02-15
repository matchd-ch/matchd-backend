import graphene
from graphene import ObjectType

from api.data import zip_city_datasource


class ZipCityType(ObjectType):
    zip = graphene.String()
    city = graphene.String()
    canton = graphene.String()


class ZipCityQuery(ObjectType):
    zip_city = graphene.List(ZipCityType)

    def resolve_zip_city(self, info, **kwargs):
        return zip_city_datasource.data
