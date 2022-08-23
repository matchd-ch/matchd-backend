from db.context.match.matching import Matching
from db.context.match.company_matching import CompanyMatching
from db.context.match.job_posting_matching import JobPostingMatching
from db.context.match.challenge_matching import ChallengeMatching
from db.context.match.student_matching import StudentMatching
from db.models.user import User


class MatchingFactory:

    def get_matching_context(self, user: User, **kwargs: dict) -> Matching:
        matching_context = CompanyMatching(user, **kwargs)

        if kwargs.get('job_posting_matching', False):
            kwargs['data'] = kwargs.pop('job_posting_matching')
            matching_context = JobPostingMatching(user, **kwargs)

        if kwargs.get('student_matching', False):
            kwargs['data'] = kwargs.pop('student_matching')
            matching_context = StudentMatching(user, **kwargs)

        if kwargs.get('challenge_matching', False):
            kwargs['data'] = kwargs.pop('challenge_matching')
            matching_context = ChallengeMatching(user, **kwargs)

        return matching_context
