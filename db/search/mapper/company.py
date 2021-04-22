from db.models import Attachment, AttachmentKey, Match, MatchType


class CompanyMatchMapper:

    def __init__(self, companies, user):
        self.companies = companies
        self.company_ids = [obj.id for obj in companies]
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
        matches = Match.objects.filter(student=self.user.student, job_posting__company_id__in=self.company_ids)
        for match in matches:
            self.matches_map[match.job_posting.company.id] = match

    def _get_attachment(self, company):
        attachment = self.attachment_map.get(company.id, None)
        if attachment is not None:
            attachment = attachment.absolute_url
        return attachment

    def _get_match_status(self, company):
        if self.matches_map.get(company.id) is not None:
            match_obj = self.matches_map.get(company.id)
            return {
                'confirmed': match_obj.complete,
                'initiator': match_obj.initiator
            }
        return None

    def _map_company(self, company):
        return {
            'id': company.id,
            'name': company.name,
            'avatar': self._get_attachment(company),
            'type': MatchType.COMPANY,
            'slug': company.slug,
            'score': company.score,
            'raw_score': company.raw_score,
            'job_posting_title': None,
            'match_status': self._get_match_status(company)
        }

    def get_matches(self):
        return [self._map_company(company) for company in self.companies]
