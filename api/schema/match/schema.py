from datetime import datetime

import graphene
from graphql_jwt.decorators import login_required
from graphene import ObjectType, InputObjectType

from api.schema.job_posting import JobPostingInput
from api.schema.profile_type import ProfileType
from db.models import ProfileState, AttachmentKey, Attachment, ProfileType as ProfileTypeModel, Skill, \
    UserLanguageRelation, Language, LanguageLevel
from db.search import Matching


def map_students(students):
    matches = []
    for student in students:
        name = '%s %s' % (student.user.first_name, student.user.last_name)
        attachment = Attachment.objects.filter(
            key=AttachmentKey.STUDENT_AVATAR,
            content_type=student.get_profile_content_type(),
            object_id=student.get_profile_id()
        ).prefetch_related('content_object', 'attachment_object')
        if len(attachment) > 0:
            attachment = attachment[0].absolute_url
        else:
            attachment = None
        if student.state == ProfileState.ANONYMOUS:
            name = student.nickname
            attachment = None
        match = {
            'name': name,
            'avatar': attachment,
            'type': student.user.type,
            'slug': student.nickname,
            'score': student.score
        }
        matches.append(match)
    return matches


def map_companies(companies):
    matches = []
    for company in companies:
        name = company.name
        attachment = Attachment.objects.prefetch_related('content_object', 'attachment_object').\
            select_related('attachment_type').filter(
                key=AttachmentKey.COMPANY_AVATAR,
                content_type=company.get_profile_content_type(),
                object_id=company.get_profile_id()
            )
        if len(attachment) > 0:
            attachment = attachment[0].absolute_url
        else:
            attachment = None
        match = {
            'name': name,
            'avatar': attachment,
            'type': company.type,
            'slug': company.slug,
            'score': company.score
        }
        matches.append(match)
    return matches


class Match(ObjectType):
    name = graphene.NonNull(graphene.String)
    avatar = graphene.String()
    type = graphene.Field(ProfileType)
    slug = graphene.NonNull(graphene.String)
    score = graphene.NonNull(graphene.Float)


class TalentMatchingInput(InputObjectType):
    job_posting = graphene.Field(JobPostingInput, required=True)
    tech_boost = graphene.Int(required=True)
    soft_boost = graphene.Int(required=True)


class MatchQuery(ObjectType):
    matches = graphene.List(
        Match,
        talent_matching=graphene.Argument(TalentMatchingInput, required=False)
    )

    @login_required
    def resolve_matches(self, info, **kwargs):
        user = info.context.user

        talent_matching = kwargs.get('talent_matching', None)
        branch = 1

        if user.type in ProfileTypeModel.valid_company_types():
            matching = Matching()
            matches = matching.find_talents(
                branch_id=branch,
                job_type_id=1,
                cultural_fits=user.company.cultural_fits.all(),
                soft_skills=user.company.soft_skills.all(),
                skills=Skill.objects.filter(id__in=[1, 4, 6, 8, 10, 12]),
                languages=[UserLanguageRelation(language=Language.objects.get(pk=5),
                                                language_level=LanguageLevel.objects.get(pk=7))],
                date_from=datetime.strptime('01.08.2021', '%d.%m.%Y').date(),
                date_to=datetime.strptime('02.10.2021', '%d.%m.%Y').date()
            )
            matches = map_students(matches)
            print('*' * 100)
            print(len(matches))
            print('*' * 100)
            return matches

        if user.type in ProfileTypeModel.valid_student_types():
            matching = Matching()
            matches = matching.find_companies(branch_id=branch, cultural_fits=user.student.cultural_fits.all(),
                                              soft_skills=user.student.soft_skills.all())
            matches = map_companies(matches)
            return matches
