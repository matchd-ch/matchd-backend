from django.conf import settings

from db.models import Student
from .base import BaseScoreCalculator


class JobPostingScoreCalculator(BaseScoreCalculator):

    def __init__(self, user, hits, soft_boost, tech_boost):
        self.user = user
        student = Student.objects.prefetch_related('languages',
                                                   'languages__language_level').get(user=user)
        super().__init__(hits, student.languages.all(), soft_boost, tech_boost)

    def add_language_score(self, hit):
        languages = hit.languages.all()
        if len(languages) == 0:
            return
        multiplier = settings.MATCHING_VALUE_LANGUAGES / len(languages) / 2    # language and level
        score = hit.score
        for language in languages:
            if language.language_id in self.language_level_map:
                score += multiplier
                level_value = self.language_level_map[language.language_id]
                # we should actually add the multiplier to the score.
                # but if one has a better language level than the one required, it should result in better score
                # This would be correct:
                # if level_value >= language.language_level.value:
                #     score += multiplier
                # One with better language skills can get a match beyond 100 %
                score += (level_value / language.language_level.value * multiplier)
        hit.score = round(score, 2)

    def highest_possible_value(self):
        value = 0
        value += settings.MATCHING_VALUE_BRANCH
        value += settings.MATCHING_VALUE_JOB_TYPE
        value += settings.MATCHING_VALUE_WORKLOAD
        value += self.soft_boost * settings.MATCHING_VALUE_CULTURAL_FITS
        value += self.soft_boost * settings.MATCHING_VALUE_SOFT_SKILLS
        value += self.tech_boost * settings.MATCHING_VALUE_SKILLS
        value += settings.MATCHING_VALUE_LANGUAGES
        value += settings.MATCHING_VALUE_DATE_OR_DATE_RANGE
        return value
