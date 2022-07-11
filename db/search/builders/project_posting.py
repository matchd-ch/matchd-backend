from db.search.builders.base import BaseParamBuilder


class ProjectPostingParamBuilder(BaseParamBuilder):

    def set_is_student(self):
        self.must_conditions.append({"bool": {"must": [{'term': {'is_student_filter': True}}]}})

    def set_is_company(self):
        self.must_conditions.append({"bool": {"must": [{'term': {'is_company_filter': True}}]}})

    def set_cultural_fits(self, cultural_fits, boost=1):
        if len(cultural_fits) == 0:
            return
        boost = boost / len(cultural_fits)
        for obj in cultural_fits:
            self.should_conditions.append({
                "bool": {
                    "should": [{
                        'terms': {
                            'cultural_fits_filter': [obj.id],
                            'boost': boost
                        }
                    }]
                }
            })

    def set_soft_skills(self, soft_skills, boost=1):
        if len(soft_skills) == 0:
            return
        boost = boost / len(soft_skills)
        for obj in soft_skills:
            self.should_conditions.append(
                {"bool": {
                    "should": [{
                        'terms': {
                            'soft_skills_filter': [obj.id],
                            'boost': boost
                        }
                    }]
                }})

    def set_project_type(self, project_type_id, boost=1):
        self.should_conditions.append({
            "bool": {
                "should": [{
                    'terms': {
                        'project_type_id_filter': [project_type_id],
                        'boost': boost
                    }
                }]
            }
        })

    def set_keywords(self, keywords, boost=1):
        if len(keywords) == 0:
            return
        boost = boost / len(keywords)
        for obj in keywords:
            self.should_conditions.append(
                self.get_condition('keywords', 'id_filter', [obj.id], boost))
