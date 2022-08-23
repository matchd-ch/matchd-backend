from graphql_relay import to_global_id

from db.models import MatchType, Match, ProfileType, Attachment, AttachmentKey


class ChallengeMatchMapper:

    def __init__(self, challenges, user):
        self.user = user
        self.challenges = challenges
        self.challenge_ids = [obj.id for obj in challenges]
        self.matches_map = {}
        self.attachment_map = {}
        self._prefetch_matches()
        self._prefetch_attachments()

    def _prefetch_attachments(self):
        attachments = Attachment.objects.filter(key=AttachmentKey.CHALLENGE_IMAGES,
                                                object_id__in=self.challenge_ids).select_related(
                                                    'content_type', 'attachment_type')

        for attachment in attachments:
            if attachment.object_id not in self.attachment_map:
                self.attachment_map[attachment.object_id] = attachment

    def _get_attachment(self, challenge):
        attachment = self.attachment_map.get(challenge.id, None)
        if attachment is not None:
            attachment = attachment.absolute_url
        else:
            attachment = Attachment.get_challenge_fallback(challenge)
            if attachment is not None:
                attachment = attachment.absolute_url
        return attachment

    def _prefetch_matches(self):
        matches = []
        if self.user.type in ProfileType.valid_company_types():
            matches = Match.objects.filter(company=self.user.company,
                                           challenge_id__in=self.challenge_ids)
        if self.user.type in ProfileType.valid_student_types():
            matches = Match.objects.filter(student=self.user.student,
                                           challenge_id__in=self.challenge_ids)
        for match in matches:
            self.matches_map[match.challenge.id] = match

    def _get_match_status(self, challenge):
        if self.matches_map.get(challenge.id) is not None:
            match_obj = self.matches_map.get(challenge.id)
            return {'confirmed': match_obj.complete, 'initiator': match_obj.initiator}
        return None

    def _map_challenge(self, challenge):
        name = None
        if challenge.company is not None:
            name = challenge.company.name
        if challenge.student is not None:
            if challenge.id in self.matches_map:
                name = f'{challenge.student.user.first_name} {challenge.student.user.last_name}'
            else:
                name = challenge.student.nickname

        return {
            'id': to_global_id('Challenge', challenge.id),
            'name': name,
            'avatar': self._get_attachment(challenge),
            'type': MatchType.CHALLENGE,
            'slug': challenge.slug,
            'score': challenge.score,
            'raw_score': challenge.raw_score,
            'title': challenge.title,
            'description': challenge.description,
            'keywords': challenge.keywords.all(),
            'match_status': self._get_match_status(challenge)
        }

    def get_matches(self):
        return [self._map_challenge(challenge) for challenge in self.challenges]
