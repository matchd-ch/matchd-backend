from db.models import Attachment, AttachmentKey, ProfileState


class MatchMapper:

    @classmethod
    def map_students(cls, students):
        # prefetch student avatars
        student_ids = [obj.id for obj in students]
        attachments = Attachment.objects.filter(
            key=AttachmentKey.STUDENT_AVATAR,
            object_id__in=student_ids
        ).select_related('content_type', 'attachment_type')
        attachment_map = {}
        for attachment in attachments:
            attachment_map[attachment.object_id] = attachment

        matches = []
        for student in students:
            name = '%s %s' % (student.user.first_name, student.user.last_name)
            attachment = attachment_map.get(student.id, None)
            if attachment is not None:
                attachment = attachment.absolute_url
            if student.state == ProfileState.ANONYMOUS:
                name = student.nickname
                attachment = None
            match = {
                'name': name,
                'avatar': attachment,
                'type': student.user.type,
                'slug': student.nickname,
                'score': student.score,
                'raw_score': student.raw_score
            }
            matches.append(match)
        return matches

    @classmethod
    def map_companies(cls, companies):
        # prefetch company avatars
        company_ids = [obj.id for obj in companies]
        attachments = Attachment.objects.filter(
            key=AttachmentKey.COMPANY_AVATAR,
            object_id__in=company_ids
        ).select_related('content_type', 'attachment_type')
        attachment_map = {}
        for attachment in attachments:
            attachment_map[attachment.object_id] = attachment

        matches = []
        for company in companies:
            name = company.name
            attachment = attachment_map.get(company.id, None)
            if attachment is not None:
                attachment = attachment.absolute_url
            match = {
                'name': name,
                'avatar': attachment,
                'type': company.type,
                'slug': company.slug,
                'score': company.score,
                'raw_score': company.raw_score
            }
            matches.append(match)
        return matches
