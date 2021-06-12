from django.conf import settings

from db.search.calculators.base import BaseScoreCalculator


class ProjectPostingScoreCalculator(BaseScoreCalculator):

    def __init__(self, user, hits, soft_boost, tech_boost):
        self.user = user
        super().__init__(hits, None, soft_boost, tech_boost)

    def add_language_score(self, hit):
        pass

    def highest_possible_value(self):
        value = 0
        value += settings.MATCHING_VALUE_TOPIC
        value += settings.MATCHING_VALUE_PROJECT_TYPE
        value += self.soft_boost * settings.MATCHING_VALUE_CULTURAL_FITS
        value += self.soft_boost * settings.MATCHING_VALUE_SOFT_SKILLS
        value += self.tech_boost * settings.MATCHING_VALUE_KEYWORDS
        return value
