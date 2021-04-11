from .base import BaseParamBuilder


class JobPostingParamBuilder(BaseParamBuilder):

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

    def set_workload(self, workload, boost=1):
        self.should_conditions.append({
                "bool": {
                    "should": [
                        {
                            # we need to include matches without a job start date set, but without boosting it
                            # null values are set to 01.01.1970 see db.models.Student (search_fields)
                            "exists": {
                                "field": "workload_filter",
                                "boost": 0
                            }
                        },
                        # boost exact workload
                        self.get_range_query('workload_filter', workload, 0, boost / 3),
                        # boost workload +- 10 %
                        self.get_range_query('workload_filter', workload, 10, boost / 3),
                        # boost workload +- 20 %
                        self.get_range_query('workload_filter', workload, 20, boost / 3)
                    ]
                }
            })

    def set_zip(self, zip_value):
        self.must_conditions.append({
                "bool": {
                    "must": {
                        "match": {
                            "zip_code_filter": {
                                "query": zip_value,
                                "boost": 0
                            }
                        }
                    }
                }
            })

    def set_cultural_fits(self, cultural_fits, boost=1):
        boost = boost / len(cultural_fits)
        for obj in cultural_fits:
            self.should_conditions.append({
                "bool": {
                    "should": [
                        {
                            'terms': {
                                'cultural_fits_filter': [obj.id],
                                'boost': boost
                            }
                        }
                    ]
                }
            })

    def set_soft_skills(self, soft_skills, boost=1):
        boost = boost / len(soft_skills)
        for obj in soft_skills:
            self.should_conditions.append({
                "bool": {
                    "should": [
                        {
                            'terms': {
                                'soft_skills_filter': [obj.id],
                                'boost': boost
                            }
                        }
                    ]
                }
            })

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
