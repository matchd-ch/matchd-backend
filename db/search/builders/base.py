from dateutil.relativedelta import relativedelta
from django.conf import settings


# pylint: disable=R0913
class BaseParamBuilder:

    def __init__(self, queryset, index, first, skip):
        self.queryset = queryset
        self.index = index
        self.first = first
        self.skip = skip
        self.must_conditions = []
        self.should_conditions = []
        self.filter_conditions = []

    def set_branch(self, branch_id, boost=1):
        if branch_id is None:
            return

        self.must_conditions.append({
            'nested': {
                "path": "branches",
                'query': {
                    'bool': {
                        'must': {
                            "terms": {
                                "branches.id_filter": [branch_id]
                            },
                        }
                    }
                },
                'boost': boost
            },
        })

    def set_job_type(self, job_type_id, boost=1):
        if job_type_id is None:
            return

        self.should_conditions.append({
            "bool": {
                "should": [{
                    'terms': {
                        'job_type_id_filter': [job_type_id],
                        'boost': boost
                    }
                }]
            }
        })

    def set_skills(self, skills, boost=1):
        if len(skills) == 0:
            return
        boost = boost / len(skills)
        for obj in skills:
            self.should_conditions.append(self.get_condition('skills', 'id_filter', [obj.id],
                                                             boost))

    def set_date_from(self, date_from, boost=1):
        if date_from is None:
            return

        boost = boost / len(settings.MATCHING_VALUE_DATE_OR_DATE_RANGE_PRECISION)
        conditions = [{
        # we need to include matches without a job start date set, but without boosting it
        # null values are set to 01.01.1970 see db.models.Student (search_fields)
            "exists": {
                "field": "job_from_date_filter",
                "boost": 0
            }
        }]
        for matching_value in settings.MATCHING_VALUE_DATE_OR_DATE_RANGE_PRECISION:
            conditions.append(
                self.get_date_range_query('job_from_date_filter', date_from, date_from,
                                          matching_value, boost))

        self.should_conditions.append({"bool": {"should": conditions}})

    def set_date_range(self, date_from, date_to, boost=1):
        if date_from is None or date_to is None:
            return

        boost = boost / len(settings.MATCHING_VALUE_DATE_OR_DATE_RANGE_PRECISION)
        conditions = [{
        # we need to include matches without a job start/end date set, but without boosting it
        # null values are set to 01.01.1970 see db.models.Student (search_fields)
            "exists": {
                "field": "job_from_date_filter",
                "boost": 0
            }
        }]
        for matching_value in settings.MATCHING_VALUE_DATE_OR_DATE_RANGE_PRECISION:
            conditions.append(
                self.get_nested_date_range_query('job_from_date_filter', 'job_to_date_filter',
                                                 date_from, date_to, matching_value, boost / 2))

        self.should_conditions.append({"bool": {"should": conditions}})

    def get_params(self):
        return {
            'index': [self.index],
            'body': {
                'query': {
                    'bool': {
                        "must": self.must_conditions,
                        "should": self.should_conditions
                    },
                }
            },
            '_source': 'pk',
        }

    def get_condition(self, path, prop, value, boost=1, condition_type='bool'):
        return {
            'nested': {
                'path': path,
                'query': {
                    condition_type: {
                        'should': [{
                            'terms': {
                                f'{path}.{prop}': value
                            }
                        }]
                    }
                },
                'boost': boost
            },
        }

    def get_workload_range_query(self, from_key, to_key, workload_from, workload_to, tolerance,
                                 boost):
        shifted_start = workload_from - tolerance
        shifted_end = workload_to + tolerance
        shifted_start = max(0, shifted_start)
        shifted_end = min(100, shifted_end)
        return {
        # boost dates within the shifted range
            "bool": {
                "must": [
                    {
                        "range": {
                            from_key: {
                                "lte": shifted_end,
                                "boost": boost
                            }
                        }
                    },
                    {
                        "range": {
                            to_key: {
                                "gte": shifted_start,
                                "boost": boost
                            }
                        }
                    },
                ]
            }
        }

    def get_date_range_query(self, key, date_from, date_to, months, boost):
        shifted_start = self.get_shifted_date(date_from, -months)
        shifted_end = self.get_shifted_date(date_to, +months)
        return {
        # boost dates within the shifted range
            "range": {
                key: {
                    "gte": shifted_start.strftime('%Y-%m-%d'),
                    "lte": shifted_end.strftime('%Y-%m-%d'),
                    "boost": boost
                }
            }
        }

    def get_nested_date_range_query(self, from_key, to_key, date_from, date_to, months, boost):
        shifted_start = self.get_shifted_date(date_from, -months)
        shifted_end = self.get_shifted_date(date_to, +months)
        return {
            'bool': {
                'should': [
                    {
        # boost start date within range
                        "range": {
                            from_key: {
                                "gte": shifted_start.strftime('%Y-%m-%d'),
                                "lte": shifted_end.strftime('%Y-%m-%d'),
                                "boost": boost
                            }
                        }
                    },
                    {
        # boost end date within range
                        "range": {
                            to_key: {
                                "gte": shifted_start.strftime('%Y-%m-%d'),
                                "lte": shifted_end.strftime('%Y-%m-%d'),
                                "boost": boost
                            }
                        }
                    }
                ]
            }
        }

    def get_shifted_date(self, date, months):
        return date + relativedelta(months=months)
