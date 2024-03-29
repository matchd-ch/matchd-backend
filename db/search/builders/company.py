from .base import BaseParamBuilder


class CompanyParamBuilder(BaseParamBuilder):

    def set_branch(self, branch_id, boost=1):
        if branch_id is None:
            return

        self.should_conditions.append({
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

    def set_cultural_fits(self, cultural_fits, boost=1):
        if len(cultural_fits) == 0:
            return
        boost = boost / len(cultural_fits)
        for obj in cultural_fits:
            self.should_conditions.append(
                self.get_condition('cultural_fits', 'id_filter', [obj.id], boost))

    def set_soft_skills(self, soft_skills, boost=1):
        if len(soft_skills) == 0:
            return
        boost = boost / len(soft_skills)
        for obj in soft_skills:
            self.should_conditions.append(
                self.get_condition('soft_skills', 'id_filter', [obj.id], boost))
