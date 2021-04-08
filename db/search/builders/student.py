from .base import BaseParamBuilder


class StudentParamBuilder(BaseParamBuilder):

    def set_branch(self, branch_id, boost=1):
        self.must_conditions.append(self.get_condition('branch', 'id_filter', [branch_id], boost))
        
    def set_job_type(self, job_type_id, boost=1):
        self.should_conditions.append(self.get_condition('job_type', 'id_filter', [job_type_id], boost))

    def set_cultural_fits(self, cultural_fits, boost=1):
        for obj in cultural_fits:
            self.should_conditions.append(self.get_condition('cultural_fits', 'id_filter', [obj.id], boost))

    def set_soft_skills(self, soft_skills, boost=1):
        for obj in soft_skills:
            self.should_conditions.append(self.get_condition('soft_skills', 'id_filter', [obj.id], boost))

    def set_skills(self, skills, boost=1):
        for obj in skills:
            self.should_conditions.append(self.get_condition('skills', 'id_filter', [obj.id], boost))

    def set_languages(self, languages, boost=1):
        for obj in languages:
            self.should_conditions.append(self.get_condition('languages', 'language_id_filter',
                                                             [obj.language.id], boost))
            self.should_conditions.append(
                self.get_condition('languages', 'language_level_concat_filter',
                                   [f'{obj.language.id}-{obj.language_level.id}'], boost))

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
                        self.get_range_query('job_from_date_filter', date_from, date_from, 0, boost),
                        # boost dates within 2 months
                        self.get_range_query('job_from_date_filter', date_from, date_from, 2, boost),
                        # boost dates within 6 months
                        self.get_range_query('job_from_date_filter', date_from, date_from, 6, boost)
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
                        self.get_nested_range_query('job_from_date_filter', 'job_to_date_filter', date_from, date_to, 0,
                                                    boost),
                        # boost dates within 2 months
                        self.get_nested_range_query('job_from_date_filter', 'job_to_date_filter', date_from, date_to, 2,
                                                    boost),
                        # boost dates within 6 months
                        self.get_nested_range_query('job_from_date_filter', 'job_to_date_filter', date_from, date_to, 6,
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
