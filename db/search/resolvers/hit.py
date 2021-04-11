from django.db.models import Q


class HitResolver:

    def __init__(self, queryset, hits):
        self.queryset = queryset
        self.hits = hits.get('hits')

    def sort_by_score(self, hit):
        return hit.score

    def resolve(self):
        scores = {}
        ids = []
        for hit in self.hits.get('hits'):
            obj_id = hit.get('_source').get('pk')
            ids.append(obj_id)
            score = hit.get('_score')
            scores[obj_id] = score

        query = Q(id__in=ids)
        result = self.queryset.filter(query)

        for obj in result:
            obj_id = str(obj.id)
            if obj_id in scores:
                obj_score = float(scores[obj_id])
                setattr(obj, 'score', obj_score)

        return sorted(list(result), key=self.sort_by_score, reverse=True)

