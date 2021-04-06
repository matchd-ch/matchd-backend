import graphene
from graphql_jwt.decorators import login_required
from graphene import ObjectType

from api.schema.profile_type import ProfileType
from db.models import ProfileState, AttachmentKey, Attachment, ProfileType as ProfileTypeModel
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


class MatchQuery(ObjectType):
    matches = graphene.List(
        Match,
        branch=graphene.ID(required=False)
    )

    @login_required
    def resolve_matches(self, info, **kwargs):
        user = info.context.user
        branch = kwargs.get('branch', None)

        if user.type in ProfileTypeModel.valid_company_types():
            matching = Matching()
            matches = matching.find_talents(branch_id=branch)
            matches = map_students(matches)
            return matches

        if user.type in ProfileTypeModel.valid_student_types():
            matching = Matching()
            matches = matching.find_companies(branch_id=branch)
            matches = map_companies(matches)
            return matches
