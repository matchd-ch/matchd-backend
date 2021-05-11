from db.models import Attachment, AttachmentKey, MatchType, Match


class JobPostingMatchMapper:

    def __init__(self, job_postings, user):
        self.job_postings = job_postings
        self.company_ids = [obj.company.id for obj in job_postings]
        self.job_posting_ids = [obj.id for obj in job_postings]
        self.user = user
        self.attachment_map = {}
        self.matches_map = {}
        self._prefetch_attachments()
        self._prefetch_matches()

    def _prefetch_attachments(self):
        attachments = Attachment.objects.filter(
            key=AttachmentKey.COMPANY_AVATAR,
            object_id__in=self.company_ids
        ).select_related('content_type', 'attachment_type')

        for attachment in attachments:
            self.attachment_map[attachment.object_id] = attachment

    def _prefetch_matches(self):
        matches = Match.objects.filter(student=self.user.student, job_posting_id__in=self.job_posting_ids)
        for match in matches:
            self.matches_map[match.job_posting.id] = match

    def _get_attachment(self, job_posting):
        attachment = self.attachment_map.get(job_posting.company.id, None)
        if attachment is not None:
            attachment = attachment.absolute_url
        else:
            attachment = Attachment.get_company_avatar_fallback(job_posting.company).absolute_url
        return attachment

    def _get_match_status(self, job_posting):
        if self.matches_map.get(job_posting.id) is not None:
            match_obj = self.matches_map.get(job_posting.id)
            return {
                'confirmed': match_obj.complete,
                'initiator': match_obj.initiator
            }
        return None

    def _map_job_posting(self, job_posting):
        return {
            'id': job_posting.id,
            'name': job_posting.company.name,
            'avatar': self._get_attachment(job_posting),
            'type': MatchType.JOB_POSTING,
            'slug': job_posting.slug,
            'score': job_posting.score,
            'raw_score': job_posting.raw_score,
            'job_posting_title': job_posting.title,
            'match_status': self._get_match_status(job_posting)
        }

    def get_matches(self):
        return [self._map_job_posting(job_posting) for job_posting in self.job_postings]
