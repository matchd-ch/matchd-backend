from db.models import Attachment, AttachmentKey, ProfileState


class MatchMapper:

    @classmethod
    def map_students(cls, students):
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

    @classmethod
    def map_companies(cls, companies):
        matches = []
        for company in companies:
            name = company.name
            attachment = Attachment.objects.prefetch_related('content_object', 'attachment_object'). \
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
