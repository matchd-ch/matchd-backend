from django.conf import settings


class JobPostingScoreCalculator:

    def __init__(self, user, hits, soft_boost, tech_boost):
        self.user = user
        self.hits = hits
        self.soft_boost = soft_boost
        self.tech_boost = tech_boost
        self.override_score = False
        self.language_level_map = {}

    def init_language_map(self):
        languages = self.user.student.languages.all()
        for language in languages:
            self.language_level_map[language.language_id] = language.language_level.value

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
                score += (level_value / language.language_level.value * multiplier)
        hit.score = round(score, 2)

    def calculate_score_multiplier(self, min_value, max_value):
        # this only happens if all hits have the same score, which is equal to max score
        # eg. only 100% matches
        if max_value - min_value == 0:
            return 1
        return 100 / (max_value - min_value) / 100

    def calculate_raw_score_multiplier(self, max_value):
        return 100 / max_value / 100

    def shift_score(self, origin_score, minimum, multiplier):
        origin_score = origin_score - minimum
        return min(1, round(origin_score * multiplier, 2))

    def shift_raw_score(self, origin_score, multiplier):
        return min(1, round(origin_score * multiplier, 2))

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
    
    def min_max_value(self):
        max_value = 0
        min_score = 1000000
        for hit in self.hits:
            self.add_language_score(hit)
            if float(hit.score) > max_value:
                max_value = hit.score
            if float(hit.score) < min_score:
                min_score = hit.score
        return min_score, max_value

    def sort_by_score(self, hit):
        return hit.score

    def annotate(self):
        self.init_language_map()
        highest_possible_value = self.highest_possible_value()
        min_value, max_value = self.min_max_value()

        # this mostly happens if all results have the same score
        if min_value == max_value:
            score_multiplier = self.calculate_score_multiplier(min_value, highest_possible_value)
        else:
            score_multiplier = self.calculate_score_multiplier(min_value, max_value)
        raw_score_multiplier = self.calculate_raw_score_multiplier(highest_possible_value)

        for hit in self.hits:
            score = self.shift_score(hit.score, min_value, score_multiplier)
            raw_score = self.shift_raw_score(hit.score, raw_score_multiplier)
            setattr(hit, 'score', score)
            setattr(hit, 'raw_score', raw_score)

        return sorted(self.hits, key=self.sort_by_score, reverse=True)