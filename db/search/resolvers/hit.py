from django.db.models import Q


class HitResolver:

    def __init__(self, queryset, hits):
        self.queryset = queryset
        self.hits = hits.get('hits')

    def resolve(self):
        scores = {}
        ids = []
        for hit in self.hits.get('hits'):
            obj_id = hit.get('_source').get('pk')
            ids.append(obj_id)
            scores[obj_id] = hit.get('_score')
        query = Q(id__in=ids)
        result = self.queryset.filter(query)
        for obj in result:
            obj_id = str(obj.id)
            if obj_id in scores:
                setattr(obj, 'score', scores[obj_id])

        def sort_by_score(x):
            return x.score
        return sorted(list(result), key=sort_by_score, reverse=True)
