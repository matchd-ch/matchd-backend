import graphene
from graphene import ObjectType

from django.db.models import Q

from api.helper import resolve_node_id
from api.helper.location import filter_correct_zip_and_city
from api.data import zip_city_datasource

from db.models import JobPosting, JobPostingState


class ZipCity(ObjectType):
    zip = graphene.NonNull(graphene.String)
    city = graphene.NonNull(graphene.String)
    canton = graphene.NonNull(graphene.String)


class ZipCityQuery(ObjectType):
    zip_city = graphene.NonNull(graphene.List(graphene.NonNull(ZipCity)))
    zip_city_jobs = graphene.NonNull(graphene.List(graphene.NonNull(ZipCity)),
                                     branch_id=graphene.String(required=False),
                                     job_type_id=graphene.String(required=False))

    def resolve_zip_city(self, info, **kwargs):
        return zip_city_datasource.data

    def resolve_zip_city_jobs(self, info, **kwargs):
        query = Q(state=JobPostingState.PUBLIC)
        branch = resolve_node_id(kwargs.get('branch_id'))
        job_type = resolve_node_id(kwargs.get('job_type_id'))

        if branch is not None:
            query &= Q(branches__in=[branch])
        if job_type is not None:
            query &= Q(job_type_id=job_type)

        job_postings = JobPosting.objects.select_related('company').filter(query).only(
            'company__zip', 'company__city')

        zip_mapping = {}
        for job_posting in job_postings:
            zip_mapping[job_posting.company.zip] = job_posting.company.city

        return filter_correct_zip_and_city(zip_mapping)
