from .base import BaseParamBuilder


class StudentParamBuilder(BaseParamBuilder):

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

    def set_branches(self, branches, boost=1):
        if len(branches) == 0:
            return

        self.must_conditions.append({
            "bool": {
                "should": [{
                    'terms': {
                        'branch_id_filter': [branch.id for branch in branches],
                        'boost': boost
                    }
                }]
            }
        })
