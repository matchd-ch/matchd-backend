from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from wagtail.search.backends import get_search_backend

from db.context.match.matching import Matching
from db.models import Challenge, ProfileType
from db.search.builders import ChallengeParamBuilder
from db.search.calculators import ChallengeScoreCalculator
from db.search.mapper import ChallengeMatchMapper
from db.search.resolvers import HitResolver

# pylint: disable=R0913


class ChallengeMatching(Matching):
    search_backend = get_search_backend()

    def __init__(self, user, **kwargs):
        super().__init__(user, **kwargs)
        self.challenge = None

    def _validate_input(self):
        challenge = self.data.get('challenge', None)
        if challenge is not None:
            challenge_id = challenge.get('id')
            self.challenge = get_object_or_404(Challenge, pk=challenge_id)

        if self.user.type in ProfileType.valid_company_types():
            if self.user.company != self.challenge.company:
                raise PermissionDenied('You are not allowed to perform this action')

        if self.user.type in ProfileType.valid_student_types():
            if self.user.student != self.challenge.student:
                raise PermissionDenied('You are not allowed to perform this action')

    def find_matches(self):
        self._validate_input()
        queryset = Challenge.get_indexed_objects()
        index = self.search_backend.get_index_for_model(queryset.model).name

        builder = ChallengeParamBuilder(queryset, index, self.first, self.skip)
        builder.set_challenge_type(self.challenge.challenge_type.id,
                                   settings.MATCHING_VALUE_CHALLENGE_TYPE)
        builder.set_keywords(self.challenge.keywords.all(),
                             self.tech_boost * settings.MATCHING_VALUE_KEYWORDS)

        cultural_fits = None
        soft_skills = None
        if self.user.type in ProfileType.valid_student_types():
            cultural_fits = self.user.student.cultural_fits.all()
            soft_skills = self.user.student.soft_skills.all()
        if self.user.type in ProfileType.valid_company_types():
            cultural_fits = self.user.company.cultural_fits.all()
            soft_skills = self.user.company.soft_skills.all()

        builder.set_cultural_fits(cultural_fits,
                                  self.soft_boost * settings.MATCHING_VALUE_CULTURAL_FITS)
        builder.set_soft_skills(soft_skills, self.soft_boost * settings.MATCHING_VALUE_SOFT_SKILLS)

        if self.challenge.company is not None:
            builder.set_is_student()
        if self.challenge.student is not None:
            builder.set_is_company()

        hits = self.search_backend.es.search(**builder.get_params())
        resolver = HitResolver(queryset, hits)
        hits = resolver.resolve()
        calculator = ChallengeScoreCalculator(self.user, hits, self.soft_boost, self.tech_boost)
        hits = calculator.annotate()
        mapper = ChallengeMatchMapper(hits, self.user)
        return mapper.get_matches()
