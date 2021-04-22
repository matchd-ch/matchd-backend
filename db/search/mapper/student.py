from db.models import Attachment, AttachmentKey, ProfileState, MatchType, Match


class StudentMatchMapper:

    def __init__(self, students, job_posting):
        self.students = students
        self.student_ids = [obj.id for obj in self.students]
        self.job_posting = job_posting
        self.attachment_map = {}
        self.matches_map = {}
        self._prefetch_attachments()
        self._prefetch_matches()

    def _prefetch_attachments(self):
        attachments = Attachment.objects.filter(
            key=AttachmentKey.STUDENT_AVATAR,
            object_id__in=self.student_ids
        ).select_related('content_type', 'attachment_type')

        for attachment in attachments:
            self.attachment_map[attachment.object_id] = attachment

    def _prefetch_matches(self):
        matches = Match.objects.filter(job_posting=self.job_posting, student_id__in=self.student_ids)
        for match in matches:
            self.matches_map[match.student.id] = match

    def _get_attachment(self, student):
        attachment = self.attachment_map.get(student.id, None)
        if attachment is not None:
            attachment = attachment.absolute_url
        if student.state == ProfileState.ANONYMOUS:
            attachment = None
        return attachment

    def _get_name(self, student):
        name = '%s %s' % (student.user.first_name, student.user.last_name)
        if student.state == ProfileState.ANONYMOUS:
            name = student.nickname
        return name

    def _get_match_status(self, student):
        if self.matches_map.get(student.id) is not None:
            match_obj = self.matches_map.get(student.id)
            return {
                'confirmed': match_obj.complete,
                'initiator': match_obj.initiator
            }
        return None

    def _map_student(self, student):
        return {
            'id': student.id,
            'slug': student.slug,
            'name': self._get_name(student),
            'avatar': self._get_attachment(student),
            'type': MatchType.STUDENT,
            'score': student.score,
            'raw_score': student.raw_score,
            'match_status': self._get_match_status(student)
        }

    def get_matches(self):
        return [self._map_student(student) for student in self.students]
