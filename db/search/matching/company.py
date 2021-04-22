from django.conf import settings
from wagtail.search.backends import get_search_backend

from db.models import Company
from db.search.builders import CompanyParamBuilder
from db.search.calculators import CompanyScoreCalculator
from db.search.mapper import CompanyMatchMapper
from db.search.resolvers import HitResolver


class CompanyMatching:
    search_backend = get_search_backend()

    def __init__(self, user, first, skip, tech_boost, soft_boost):
        self.user = user
        self.first = first
        self.skip = skip
        self.tech_boost = tech_boost
        self.soft_boost = soft_boost

    def find_matches(self):
        queryset = Company.get_indexed_objects()
        index = self.search_backend.get_index_for_model(queryset.model).name

        builder = CompanyParamBuilder(queryset, index, self.first, self.skip)
        builder.set_branch(self.user.student.branch_id, settings.MATCHING_VALUE_BRANCH + 1)
        builder.set_cultural_fits(self.user.student.cultural_fits.all(),
                                  self.soft_boost * settings.MATCHING_VALUE_CULTURAL_FITS)
        builder.set_soft_skills(self.user.student.soft_skills.all(),
                                self.soft_boost * settings.MATCHING_VALUE_SOFT_SKILLS)

        hits = self.search_backend.es.search(**builder.get_params())
        resolver = HitResolver(queryset, hits)
        hits = resolver.resolve()
        calculator = CompanyScoreCalculator(hits, None, self.soft_boost, self.tech_boost)
        hits = calculator.annotate()

        mapper = CompanyMatchMapper(hits, self.user)
        return mapper.get_matches()
