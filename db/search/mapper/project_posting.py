from db.models import MatchType, Match, ProfileType, Attachment, AttachmentKey


class ProjectPostingMatchMapper:

    def __init__(self, project_postings, user):
        self.user = user
        self.project_postings = project_postings
        self.project_posting_ids = [obj.id for obj in project_postings]
        self.matches_map = {}
        self.attachment_map = {}
        self._prefetch_matches()
        self._prefetch_attachments()

    def _prefetch_attachments(self):
        attachments = Attachment.objects.filter(
            key=AttachmentKey.PROJECT_POSTING_IMAGES,
            object_id__in=self.project_posting_ids
        ).select_related('content_type', 'attachment_type')

        for attachment in attachments:
            if attachment.object_id not in self.attachment_map:
                self.attachment_map[attachment.object_id] = attachment

    def _get_attachment(self, project_posting):
        attachment = self.attachment_map.get(project_posting.id, None)
        if attachment is not None:
            attachment = attachment.absolute_url
        else:
            attachment = Attachment.get_project_posting_fallback(project_posting)
            if attachment is not None:
                attachment = attachment.absolute_url
        return attachment

    def _prefetch_matches(self):
        matches = []
        if self.user.type in ProfileType.valid_company_types():
            matches = Match.objects.filter(company=self.user.company, project_posting_id__in=self.project_posting_ids)
        if self.user.type in ProfileType.valid_student_types():
            matches = Match.objects.filter(student=self.user.student, project_posting_id__in=self.project_posting_ids)
        for match in matches:
            self.matches_map[match.project_posting.id] = match

    def _get_match_status(self, project_posting):
        if self.matches_map.get(project_posting.id) is not None:
            match_obj = self.matches_map.get(project_posting.id)
            return {
                'confirmed': match_obj.complete,
                'initiator': match_obj.initiator
            }
        return None

    def _map_project_posting(self, project_posting):
        name = None
        if project_posting.company is not None:
            name = project_posting.company.name
        if project_posting.student is not None:
            if project_posting.id in self.matches_map:
                name = f'{project_posting.student.user.first_name} {project_posting.student.user.last_name}'
            else:
                name = project_posting.student.nickname

        return {
            'id': project_posting.id,
            'name': name,
            'avatar': self._get_attachment(project_posting),
            'type': MatchType.PROJECT_POSTING,
            'slug': project_posting.slug,
            'score': project_posting.score,
            'raw_score': project_posting.raw_score,
            'title': project_posting.title,
            'description': project_posting.description,
            'keywords': project_posting.keywords.all(),
            'match_status': self._get_match_status(project_posting)
        }

    def get_matches(self):
        return [self._map_project_posting(project_posting) for project_posting in self.project_postings]
