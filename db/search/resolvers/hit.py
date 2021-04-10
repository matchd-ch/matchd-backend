from django.db.models import Q


class HitResolver:

    def __init__(self, queryset, hits, maximum_possible_score):
        self.queryset = queryset
        self.hits = hits.get('hits')
        self.score_multiplier = 1
        self.raw_score_multiplier = 1
        self.maximum_possible_score = maximum_possible_score
        self.calculate_raw_score_multiplier()
        self.override_score = False

    def resolve(self):
        scores = {}
        ids = []
        max_score = 0
        min_score = 1000000
        for hit in self.hits.get('hits'):
            obj_id = hit.get('_source').get('pk')
            ids.append(obj_id)
            score = hit.get('_score')
            scores[obj_id] = score
            if float(score) > max_score:
                max_score = score
            if float(score) < min_score:
                min_score = score

        # this mostly happens if all results have the same score
        if max_score == min_score:
            self.calculate_score_multiplier(self.maximum_possible_score, min_score)
        else:
            self.calculate_score_multiplier(max_score, min_score)

        query = Q(id__in=ids)
        result = self.queryset.filter(query)

        for obj in result:
            obj_id = str(obj.id)
            if obj_id in scores:
                if not self.override_score:
                    setattr(obj, 'score', self.shift_score(float(scores[obj_id]), min_score))
                else:
                    setattr(obj, 'score', 1)
                setattr(obj, 'raw_score', self.shift_raw_score(round(float(scores[obj_id]), 2)))

        def sort_by_score(value):
            return value.score
        return sorted(list(result), key=sort_by_score, reverse=True)

    def calculate_score_multiplier(self, max_score, min_score):
        # this only happens if all hits have the same score, which is equal to max score
        # eg. only 100% matches
        if max_score - min_score == 0:
            self.score_multiplier = 1
            self.override_score = True
            return
        self.score_multiplier = 100 / (max_score - min_score) / 100

    def calculate_raw_score_multiplier(self):
        self.raw_score_multiplier = 100 / self.maximum_possible_score / 100

    def shift_score(self, origin_score, minimum):
        origin_score = origin_score - minimum
        return min(1, round(origin_score * self.score_multiplier, 2))

    def shift_raw_score(self, origin_score):
        return min(1, round(origin_score * self.raw_score_multiplier, 2))
