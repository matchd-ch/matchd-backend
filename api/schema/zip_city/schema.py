import graphene
from graphene import ObjectType, InputObjectType

from django.db.models import Q

from api.data import zip_city_datasource

from db.models import JobPosting, JobPostingState


class ZipCity(ObjectType):
    zip = graphene.NonNull(graphene.String)
    city = graphene.NonNull(graphene.String)
    canton = graphene.NonNull(graphene.String)


class ZipCityInput(InputObjectType):
    zip = graphene.String(required=True)


class ZipCityQuery(ObjectType):
    zip_city = graphene.NonNull(graphene.List(graphene.NonNull(ZipCity)))
    zip_city_jobs = graphene.NonNull(graphene.List(graphene.NonNull(ZipCity)),
                                     branch_id=graphene.ID(required=False),
                                     job_type_id=graphene.ID(required=False))

    def resolve_zip_city(self, info, **kwargs):
        return zip_city_datasource.data

    def resolve_zip_city_jobs(self, info, **kwargs):
        query = Q(state=JobPostingState.PUBLIC)
        branch = kwargs.get('branch_id')
        job_type = kwargs.get('job_type_id')
        if branch is not None:
            query &= Q(branches__in=[branch])
        if job_type is not None:
            query &= Q(job_type_id=job_type)
        job_postings = JobPosting.objects.select_related('company').filter(query).only(
            'company__zip', 'company__city')
        zip_mapping = {}
        for job_posting in job_postings:
            zip_mapping[job_posting.company.zip] = job_posting.company.city
        zip_data = zip_city_datasource.data
        result = []

        # assume the following job posting zip values
        # zip_mapping = {'9000': 'St. Gallen', '9470': 'Buchs SG'}
        #
        # if we only match the zip value we will end up with the following list, which is not correct:
        # [{
        #     "zip": "9000",
        #     "city": "St. Gallen",
        #     "canton": "SG"
        # },
        # {
        #     "zip": "9470",
        #     "city": "Buchs SG",
        #     "canton": "SG"
        # },
        # {
        #     "zip": "9470",
        #     "city": "Werdenberg",  # should not be in the result
        #     "canton": "SG"
        # }]
        #
        # to avoid this, we so also check the canton value
        for obj in zip_data:
            data_zip = str(obj.get('zip'))
            if data_zip in zip_mapping:
                city_canton = zip_mapping[data_zip].split(' ')
                city_value = city_canton[0]
                canton_value = ''
                if len(city_canton) > 1:
                    canton_value = city_canton[-1]
                data_canton = obj.get('canton')
                if canton_value == data_canton:
                    if city_value == obj.get('city').split(f' {data_canton}')[0]:
                        result.append(obj)
                else:
                    if zip_mapping[data_zip] == obj.get('city'):
                        result.append(obj)
        return result
