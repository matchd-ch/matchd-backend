from django.db.models import Q


class HitResolver:

    def __init__(self, queryset, hits):
        self.queryset = queryset
        self.hits = hits.get('hits')

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
        multiplier = 100 / (max_score - min_score) / 100
        raw_multiplier = 100 / max_score / 100
        query = Q(id__in=ids)
        result = self.queryset.filter(query)

        def shift_score(origin_score, m, minimum):
            origin_score = origin_score - minimum
            return round(origin_score * m, 2)

        def shift_raw_score(origin_score, m):
            return origin_score * m

        for obj in result:
            obj_id = str(obj.id)
            if obj_id in scores:
                setattr(obj, 'score', shift_score(float(scores[obj_id]), multiplier, min_score))
                setattr(obj, 'raw_score', shift_raw_score(round(float(scores[obj_id]), 2), raw_multiplier))

        def sort_by_score(x):
            return x.score
        return sorted(list(result), key=sort_by_score, reverse=True)
