from .base import BaseParamBuilder


class JobPostingParamBuilder(BaseParamBuilder):

    def set_job_type(self, job_type_id, boost=1):
        self.should_conditions.append(self.get_condition('job_type', 'id_filter', [job_type_id], boost))

    def set_skills(self, skills, boost=1):
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
                        self.get_range_query('workload_filter', workload, 0, boost),
                        # boost workload +- 10 %
                        self.get_range_query('workload_filter', workload, 10, boost),
                        # boost workload +- 20 %
                        self.get_range_query('workload_filter', workload, 20, boost)
                    ]
                }
            })

    def set_languages(self, languages, boost=1):
        for obj in languages:
            self.should_conditions.append(self.get_condition('languages', 'language_id_filter', [obj.language.id], boost))
            # matching on language level is disabled for now,
            # see db.search.matching (calculate_job_posting_matching_max_score)
            # self.should_conditions.append(
            #     self.get_condition('languages', 'language_level_concat_filter',
            #                        [f'{obj.language.id}-{obj.language_level.id}'], boost))

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
                        self.get_date_range_query('job_from_date_filter', date_from, date_from, 0, boost),
                        # boost dates within 2 months
                        self.get_date_range_query('job_from_date_filter', date_from, date_from, 2, boost),
                        # boost dates within 6 months
                        self.get_date_range_query('job_from_date_filter', date_from, date_from, 6, boost)
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
                        self.get_nested_date_range_query('job_from_date_filter', 'job_to_date_filter', date_from, date_to, 0,
                                                         boost),
                        # boost dates within 2 months
                        self.get_nested_date_range_query('job_from_date_filter', 'job_to_date_filter', date_from, date_to, 2,
                                                         boost),
                        # boost dates within 6 months
                        self.get_nested_date_range_query('job_from_date_filter', 'job_to_date_filter', date_from, date_to, 6,
                                                         boost)
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
