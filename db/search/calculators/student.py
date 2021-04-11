from django.conf import settings

from db.search.calculators import BaseScoreCalculator


class StudentScoreCalculator(BaseScoreCalculator):

    def __init__(self, job_posting, hits, soft_boost, tech_boost):
        self.job_posting = job_posting
        super().__init__(hits, job_posting.languages.all(), soft_boost, tech_boost)

    def add_language_score(self, hit):
        languages = hit.languages.all()
        multiplier = settings.MATCHING_VALUE_LANGUAGES / len(languages) / 2  # language and level
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
                score += (language.language_level.value / level_value * multiplier)
        hit.score = round(score, 2)

    def highest_possible_value(self):
        value = 0
        value += settings.MATCHING_VALUE_BRANCH
        value += settings.MATCHING_VALUE_JOB_TYPE
        value += self.soft_boost * settings.MATCHING_VALUE_CULTURAL_FITS
        value += self.soft_boost * settings.MATCHING_VALUE_SOFT_SKILLS
        value += self.tech_boost * settings.MATCHING_VALUE_SKILLS
        value += settings.MATCHING_VALUE_LANGUAGES
        value += settings.MATCHING_VALUE_DATE_OR_DATE_RANGE
        return value
