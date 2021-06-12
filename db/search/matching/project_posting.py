from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from wagtail.search.backends import get_search_backend

from db.models import ProjectPosting, ProfileType
from db.search.builders import ProjectPostingParamBuilder
from db.search.calculators import ProjectPostingScoreCalculator
from db.search.mapper import ProjectPostingMatchMapper
from db.search.resolvers import HitResolver


class ProjectPostingMatching:
    search_backend = get_search_backend()

    def __init__(self, user, data, first, skip, tech_boost, soft_boost):
        self.user = user
        self.data = data
        self.first = first
        self.skip = skip
        self.tech_boost = tech_boost
        self.soft_boost = soft_boost
        self.project_posting = None

    def _validate_input(self):
        project_posting = self.data.get('project_posting', None)
        if project_posting is not None:
            project_posting_id = project_posting.get('id')
            self.project_posting = get_object_or_404(ProjectPosting, pk=project_posting_id)

        if self.user.type in ProfileType.valid_company_types():
            if self.user.company != self.project_posting.company:
                raise PermissionDenied('You are not allowed to perform this action')

        if self.user.type in ProfileType.valid_student_types():
            if self.user.student != self.project_posting.student:
                raise PermissionDenied('You are not allowed to perform this action')

    def find_matches(self):
        self._validate_input()
        queryset = ProjectPosting.get_indexed_objects()
        index = self.search_backend.get_index_for_model(queryset.model).name

        builder = ProjectPostingParamBuilder(queryset, index, self.first, self.skip)
        builder.set_project_type(self.project_posting.project_type.id)
        builder.set_topic(self.project_posting.topic.id)
        builder.set_keywords(self.project_posting.keywords.all())

        if self.project_posting.company is not None:
            builder.set_is_student()
        if self.project_posting.student is not None:
            builder.set_is_company()

        hits = self.search_backend.es.search(**builder.get_params())
        resolver = HitResolver(queryset, hits)
        hits = resolver.resolve()
        calculator = ProjectPostingScoreCalculator(self.user, hits, self.soft_boost, self.tech_boost)
        hits = calculator.annotate()
        mapper = ProjectPostingMatchMapper(hits, self.user)
        return mapper.get_matches()
