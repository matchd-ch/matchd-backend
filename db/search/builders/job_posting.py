from django.conf import settings

from .base import BaseParamBuilder


class JobPostingParamBuilder(BaseParamBuilder):

    def set_workload(self, workload, boost=1):
        boost = boost / len(settings.MATCHING_VALUE_WORKLOAD_PRECISION)
        conditions = [{
        # we need to include matches without a job start date set, but without boosting it
        # null values are set to 01.01.1970 see db.models.Student (search_fields)
            "exists": {
                "field": "workload_filter",
                "boost": 0
            }
        }]
        for matching_value in settings.MATCHING_VALUE_WORKLOAD_PRECISION:
            conditions.append(
                self.get_range_query('workload_filter', workload, matching_value, boost))

        self.should_conditions.append({"bool": {"should": conditions}})

    def set_zip(self, zip_value):
        self.must_conditions.append(
            {"bool": {
                "must": {
                    "match": {
                        "zip_code_filter": {
                            "query": zip_value,
                            "boost": 0
                        }
                    }
                }
            }})

    def set_cultural_fits(self, cultural_fits, boost=1):
        if len(cultural_fits) == 0:
            return
        boost = boost / len(cultural_fits)
        for obj in cultural_fits:
            self.should_conditions.append({
                "bool": {
                    "should": [{
                        'terms': {
                            'cultural_fits_filter': [obj.id],
                            'boost': boost
                        }
                    }]
                }
            })

    def set_soft_skills(self, soft_skills, boost=1):
        if len(soft_skills) == 0:
            return
        boost = boost / len(soft_skills)
        for obj in soft_skills:
            self.should_conditions.append(
                {"bool": {
                    "should": [{
                        'terms': {
                            'soft_skills_filter': [obj.id],
                            'boost': boost
                        }
                    }]
                }})
