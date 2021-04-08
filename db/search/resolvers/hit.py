from django.db.models import Q


class HitResolver:

    def __init__(self, queryset, hits):
        self.queryset = queryset
        self.hits = hits.get('hits')

    def resolve(self):
        scores = {}
        ids = []
        max_score = 0
        for hit in self.hits.get('hits'):
            obj_id = hit.get('_source').get('pk')
            ids.append(obj_id)
            score = hit.get('_score')
            scores[obj_id] = score
            if float(score) > max_score:
                max_score = score
        multiplier = 100 / max_score / 100
        query = Q(id__in=ids)
        result = self.queryset.filter(query)
        for obj in result:
            obj_id = str(obj.id)
            if obj_id in scores:
                setattr(obj, 'score', round(float(scores[obj_id]) * multiplier, 2))

        def sort_by_score(x):
            return x.score
        return sorted(list(result), key=sort_by_score, reverse=True)
