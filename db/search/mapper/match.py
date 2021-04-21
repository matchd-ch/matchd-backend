from db.models import Attachment, AttachmentKey, ProfileState, MatchType, Match


class MatchMapper:

    @classmethod
    def map_students(cls, students, job_posting):
        # prefetch student avatars
        student_ids = [obj.id for obj in students]
        attachments = Attachment.objects.filter(
            key=AttachmentKey.STUDENT_AVATAR,
            object_id__in=student_ids
        ).select_related('content_type', 'attachment_type')

        matches = Match.objects.filter(job_posting=job_posting, student_id__in=student_ids)
        matches_map = {}
        for match in matches:
            matches_map[match.student.id] = match

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
                'id': student.id,
                'slug': student.slug,
                'name': name,
                'avatar': attachment,
                'type': MatchType.STUDENT,
                'score': student.score,
                'raw_score': student.raw_score,
            }
            if matches_map.get(student.id) is not None:
                match_obj = matches_map.get(student.id)
                match['match_status'] = {
                    'confirmed': match_obj.complete,
                    'initiator': match_obj.initiator
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

    @classmethod
    def map_job_postings(cls, job_postings, user):
        print(user)
        # prefetch company avatars
        company_ids = [obj.company.id for obj in job_postings]
        attachments = Attachment.objects.filter(
            key=AttachmentKey.COMPANY_AVATAR,
            object_id__in=company_ids
        ).select_related('content_type', 'attachment_type')

        attachment_map = {}
        for attachment in attachments:
            attachment_map[attachment.object_id] = attachment

        attachment_map = {}
        for attachment in attachments:
            attachment_map[attachment.object_id] = attachment

        job_posting_ids = [obj.id for obj in job_postings]
        matches = Match.objects.filter(student=user.student, job_posting_id__in=job_posting_ids)
        matches_map = {}
        for match in matches:
            matches_map[match.job_posting.id] = match

        matches = []
        for job_posting in job_postings:
            name = job_posting.company.name
            attachment = attachment_map.get(job_posting.company.id, None)
            if attachment is not None:
                attachment = attachment.absolute_url
            match = {
                'id': job_posting.id,
                'name': name,
                'avatar': attachment,
                'type': MatchType.JOB_POSTING,
                'slug': job_posting.slug,
                'score': job_posting.score,
                'raw_score': job_posting.raw_score,
                'job_posting_title': job_posting.title
            }
            if matches_map.get(job_posting.id) is not None:
                match_obj = matches_map.get(job_posting.id)
                match['match_status'] = {
                    'confirmed': match_obj.complete,
                    'initiator': match_obj.initiator
                }
            matches.append(match)
        return matches
