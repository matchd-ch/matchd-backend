import graphene
import random
from django.db.models import Q
from graphene import ObjectType

from api.schema.profile_type import ProfileType
from db.models import Student as StudentModel, ProfileState, AttachmentKey, Attachment


def dummy_matches():
    query = Q(state=ProfileState.PUBLIC)
    query |= Q(state=ProfileState.ANONYMOUS)
    students = StudentModel.objects.filter(query)
    return students


class Match(ObjectType):
    name = graphene.NonNull(graphene.String)
    avatar = graphene.String()
    type = graphene.Field(ProfileType)
    slug = graphene.NonNull(graphene.String)
    score = graphene.NonNull(graphene.Float)


class MatchQuery(ObjectType):
    matches = graphene.List(Match)

    def resolve_matches(self, info, **kwargs):
        students = dummy_matches()
        matches = []
        for student in students:
            name = '%s %s' % (student.user.first_name, student.user.last_name)
            if student.state == ProfileState.ANONYMOUS:
                name = student.nickname

            attachment = Attachment.objects.filter(
                key=AttachmentKey.STUDENT_AVATAR,
                content_type=student.get_profile_content_type(),
                object_id=student.get_profile_id()
            ).prefetch_related('content_object', 'attachment_object')

            if len(attachment) > 0:
                attachment = attachment[0].absolute_url
            else:
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
