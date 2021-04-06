from .base import BaseParamBuilder


class StudentParamBuilder(BaseParamBuilder):

    def set_branch(self, branch_id, boost=1):
        self.must.append({
            'nested': {
                "path": "branch",
                'query': {
                    'bool': {
                        'must': {
                            "terms": {"branch.id_filter": [branch_id]},
                        }
                    }
                },
                'boost': boost
            },
        })

    def set_cultural_fits(self, cultural_fits, boost=1):
        for obj in cultural_fits:
            self.should.append({
                'nested': {
                    "path": "cultural_fits",
                    'query': {
                        'bool': {
                            'should': {
                                "terms": {"cultural_fits.id_filter": [obj.id]},
                            }
                        }
                    },
                    'boost': boost
                },
            })

    def set_soft_skills(self, soft_skills, boost=1):
        for obj in soft_skills:
            self.should.append({
                'nested': {
                    "path": "soft_skills",
                    'query': {
                        'bool': {
                            'should': {
                                "terms": {"soft_skills.id_filter": [obj.id]},
                            }
                        }
                    },
                    'boost': boost
                },
            })

    def get_params(self):
        return {
            'index': [self.index],
            'body': {
                'query': {
                    'bool': {
                        "must": self.must,
                        "should": self.should
                    },
                }
            },
            '_source': 'pk',
            'stored_fields': 'pk'
        }
