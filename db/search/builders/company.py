from .base import BaseParamBuilder


class CompanyParamBuilder(BaseParamBuilder):

    def set_branch(self, branch_id):
        self.conditions.append({
            'nested': {
                "path": "branches",
                'query': {
                    'bool': {
                        'must': {
                            "terms": {"branches.id_filter": [branch_id]},
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
