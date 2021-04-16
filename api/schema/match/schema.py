from datetime import datetime

import graphene
from django.core.exceptions import PermissionDenied
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required
from graphene import ObjectType, InputObjectType
from django.utils.translation import gettext as _

from api.schema.branch import BranchInput
from api.schema.company import CompanyInput
from api.schema.student import StudentInput
from api.schema.zip_city import ZipCityInput
from api.schema.job_posting import JobPostingInput
from api.schema.job_type import JobTypeInput
from db.models import MatchType as MatchTypeModel, ProfileType, Student, Company, Match as MatchModel
from db.models.match import MatchInitiator
from db.search.matching import JobPostingMatching, StudentMatching

MatchType = graphene.Enum.from_enum(MatchTypeModel)


class Match(ObjectType):
    id = graphene.ID()
    slug = graphene.NonNull(graphene.String)
    name = graphene.NonNull(graphene.String)
    type = graphene.NonNull(MatchType)
    avatar = graphene.String()
    score = graphene.NonNull(graphene.Float)
    raw_score = graphene.NonNull(graphene.Float)
    job_posting_title = graphene.String()


class StudentMatchingInput(InputObjectType):
    job_posting = graphene.Field(JobPostingInput, required=True)


class JobPostingMatchingInput(InputObjectType):
    branch = graphene.Field(BranchInput, required=False)
    job_type = graphene.Field(JobTypeInput, required=False)
    workload = graphene.Int(required=False)
    zip = graphene.Field(ZipCityInput, required=False)


class MatchQuery(ObjectType):
    matches = graphene.List(
        Match,
        first=graphene.Int(required=False, default_value=100),
        skip=graphene.Int(required=False, default_value=0),
        tech_boost=graphene.Int(required=False, default_value=3),
        soft_boost=graphene.Int(required=False, default_value=3),
        job_posting_matching=graphene.Argument(JobPostingMatchingInput, required=False),
        student_matching=graphene.Argument(StudentMatchingInput, required=False)
    )

    @login_required
    def resolve_matches(self, info, **kwargs):
        user = info.context.user
        first = kwargs.get('first')
        skip = kwargs.get('skip')

        # normalize boost
        soft_boost = max(min(kwargs.get('soft_boost', 1), 5), 1)
        tech_boost = max(min(kwargs.get('tech_boost', 1), 5), 1)

        job_posting_matching = kwargs.get('job_posting_matching', None)
        if job_posting_matching is not None:
            matching = JobPostingMatching(user, job_posting_matching, first, skip, tech_boost, soft_boost)
            return matching.find_matches()

        student_matching = kwargs.get('student_matching', None)
        if student_matching is not None:
            matching = StudentMatching(user, student_matching, first, skip, tech_boost, soft_boost)
            return matching.find_matches()
        return []


class MatchInput(graphene.InputObjectType):
    student = graphene.Field(StudentInput)
    company = graphene.Field(CompanyInput)


class CreateMatch(Output, graphene.Mutation):

    confirmed = graphene.Boolean(default_value=False)

    class Arguments:
        match = MatchInput(description=_('MatchInput'), required=True)

    class Meta:
        description = _('Initiate or confirm Matching')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user

        is_student = False
        is_company = False

        student = None
        company = None

        if user.type in ProfileType.valid_student_types():
            is_student = True
            student = user.student
        if user.type in ProfileType.valid_company_types():
            is_company = True
            company = user.company

        if not is_student and not is_company:
            raise PermissionDenied('You are not allowed to perform this action')

        match = data.get('match')

        target = None
        match_obj = None
        if is_company:
            target = match.get('student').get('id')
            target = Student.objects.get(pk=target)
            match_obj, created = MatchModel.objects.get_or_create(company=company, student=target)
            match_obj.company_confirmed = True
            if not created:
                match_obj.date_confirmed = datetime.now()
            else:
                match_obj.initiator = MatchInitiator.COMPANY
            match_obj.save()
        if is_student:
            target = match.get('company').get('id')
            target = Company.objects.get(pk=target)
            match_obj, created = MatchModel.objects.get_or_create(student=student, company=target)
            match_obj.student_confirmed = True
            if not created:
                match_obj.date_confirmed = datetime.now()
                match_obj.complete = True
            else:
                match_obj.initiator = MatchInitiator.STUDENT
            match_obj.save()

        if match_obj is None:
            return CreateMatch(success=False, errors=None, confirmed=False)

        return CreateMatch(success=True, errors=None,
                           confirmed=match_obj.complete)


class MatchMutation(graphene.ObjectType):
    match = CreateMatch.Field()
