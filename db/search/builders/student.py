from .base import BaseParamBuilder


class StudentParamBuilder(BaseParamBuilder):

    def set_branch(self, branch_id):
        self.conditions.append({
            'nested': {
                "path": "branch",
                'query': {
                    'bool': {
                        'must': {
                            "terms": {"branch.id_filter": [branch_id]},
                        }
                    }
                }
            },
        })

    def get_params(self):
        return {
            'index': [self.index],
            'body': {
                'query': {
                    'bool': {
                        "filter": self.conditions
                    },
                }
            },
            '_source': 'pk',
            'stored_fields': 'pk'
        }
