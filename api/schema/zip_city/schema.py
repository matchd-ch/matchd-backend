import graphene
from graphene import ObjectType

from api.data import zip_city_datasource
from db.models import JobPosting, JobPostingState


class ZipCity(ObjectType):
    zip = graphene.NonNull(graphene.String)
    city = graphene.NonNull(graphene.String)
    canton = graphene.NonNull(graphene.String)


class ZipCityQuery(ObjectType):
    zip_city = graphene.NonNull(graphene.List(graphene.NonNull(ZipCity)))
    zip_city_jobs = graphene.NonNull(graphene.List(graphene.NonNull(ZipCity)))

    def resolve_zip_city(self, info, **kwargs):
        return zip_city_datasource.data

    def resolve_zip_city_jobs(self, info, **kwargs):
        job_postings = JobPosting.objects.select_related('company').filter(state=JobPostingState.PUBLIC).\
            only('company__zip').values_list('company__zip', flat=True)
        zip_values = list(job_postings)
        zip_data = zip_city_datasource.data
        return [obj for obj in zip_data if str(obj.get('zip')) in zip_values]



