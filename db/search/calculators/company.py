from django.conf import settings

from db.search.calculators.base import BaseScoreCalculator


class CompanyScoreCalculator(BaseScoreCalculator):

    def add_language_score(self, hit):
        pass

    def highest_possible_value(self):
        value = 0
        value += settings.MATCHING_VALUE_BRANCH
        value += self.soft_boost * settings.MATCHING_VALUE_CULTURAL_FITS
        value += self.soft_boost * settings.MATCHING_VALUE_SOFT_SKILLS
        return value
