from dateutil.relativedelta import relativedelta


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
        self.should_conditions.append({
            "bool": {
                "should": [
                    {
                        'terms': {
                            'branch_id_filter': [branch_id],
                            'boost': boost
                        }
                    }
                ]
            }
        })

    def set_job_type(self, job_type_id, boost=1):
        self.should_conditions.append({
            "bool": {
                "should": [
                    {
                        'terms': {
                            'job_type_id_filter': [job_type_id],
                            'boost': boost
                        }
                    }
                ]
            }
        })

    def set_skills(self, skills, boost=1):
        boost = boost / len(skills)
        for obj in skills:
            self.should_conditions.append(self.get_condition('skills', 'id_filter', [obj.id], boost))

    def set_date_from(self, date_from, boost=1):
        self.should_conditions.append(
            {
                "bool": {
                    "should": [
                        {
                            # we need to include matches without a job start date set, but without boosting it
                            # null values are set to 01.01.1970 see db.models.Student (search_fields)
                            "exists": {
                                "field": "job_from_date_filter",
                                "boost": 0
                            }
                        },
                        # boost exact dates
                        self.get_date_range_query('job_from_date_filter', date_from, date_from, 0, boost / 3),
                        # boost dates within 2 months
                        self.get_date_range_query('job_from_date_filter', date_from, date_from, 2, boost / 3),
                        # boost dates within 6 months
                        self.get_date_range_query('job_from_date_filter', date_from, date_from, 6, boost / 3)
                    ]
                }
            }
        )

    def set_date_range(self, date_from, date_to, boost=1):
        self.should_conditions.append(
            {
                "bool": {
                    "should": [
                        {
                            # we need to include matches without a job start/end date set, but without boosting it
                            # null values are set to 01.01.1970 see db.models.Student (search_fields)
                            "exists": {
                                "field": "job_from_date_filter",
                                "boost": 0
                            }
                        },
                        # boost exact dates
                        self.get_nested_date_range_query('job_from_date_filter', 'job_to_date_filter', date_from,
                                                         date_to, 0, boost / 6),
                        # boost dates within 2 months
                        self.get_nested_date_range_query('job_from_date_filter', 'job_to_date_filter', date_from,
                                                         date_to, 2, boost / 6),
                        # boost dates within 6 months
                        self.get_nested_date_range_query('job_from_date_filter', 'job_to_date_filter', date_from,
                                                         date_to, 6, boost / 6)
                    ]
                }
            }
        )

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
            'stored_fields': 'pk',
            'size': self.first,
            'from_': self.skip
        }

    def get_condition(self, path, prop, value, boost=1, condition_type='bool'):
        return {
            'nested': {
                'path': path,
                'query': {
                    condition_type: {
                        'should': [
                            {
                                'terms': {
                                    f'{path}.{prop}': value
                                }
                            }
                        ]
                    }
                },
                'boost': boost
            },
        }

    def get_range_query(self, key, value, shift, boost):
        shifted_start = value - shift
        shifted_end = value + shift
        shifted_start = max(0, shifted_start)
        shifted_end = min(100, shifted_end)
        return {
            # boost dates within the shifted range
            "range": {
                key: {
                    "gte": shifted_start,
                    "lte": shifted_end,
                    "boost": boost
                }
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
