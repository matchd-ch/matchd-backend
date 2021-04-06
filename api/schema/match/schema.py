import random
import graphene
from django.db.models import Q
from graphene import ObjectType

from api.schema.profile_type import ProfileType
from db.models import Student as StudentModel, ProfileState, AttachmentKey, Attachment, \
    ProfileType as ProfileTypeModel, Company as CompanyModel


def dummy_student_matches():
    query = Q(state=ProfileState.PUBLIC)
    query |= Q(state=ProfileState.ANONYMOUS)
    students = StudentModel.objects.filter(query)
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
            'score': round(random.randint(0, 100) / 100, 2)
        }
        matches.append(match)
    return matches


def dummy_company_matches():
    companies = CompanyModel.objects.filter(state=ProfileState.PUBLIC)
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
            'score': round(random.randint(0, 100) / 100, 2)
        }
        matches.append(match)
    return matches


class Match(ObjectType):
    name = graphene.NonNull(graphene.String)
    avatar = graphene.String()
    type = graphene.Field(ProfileType)
    slug = graphene.NonNull(graphene.String)
    score = graphene.NonNull(graphene.Float)


class MatchQuery(ObjectType):
    matches = graphene.List(Match)

    def resolve_matches(self, info, **kwargs):
        user = info.context.user

        if user.type in ProfileTypeModel.valid_company_types():
            matches = dummy_student_matches()
        else:
            matches = dummy_company_matches()

        return matches
