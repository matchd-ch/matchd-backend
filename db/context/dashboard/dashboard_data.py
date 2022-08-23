from abc import ABC

from db.models.user import User


class DashboardData(ABC):

    def __init__(self, user: User) -> None:
        self._data = {
            'job_postings': self.collect_job_postings(user),
            'challenges': self.collect_challenges(user),
            'latest_job_postings': self.collect_latest_job_postings(user),
            'latest_challenges': self.collect_latest_challenges(user),
            'requested_matches': self.collect_requested_matches(user),
            'unconfirmed_matches': self.collect_unconfirmed_matches(user),
            'confirmed_matches': self.collect_confirmed_matches(user),
            'challenge_matches': self.collect_challenge_matches(user),
        }

    @property
    def data(self) -> dict:
        return self._data

    def collect_job_postings(self, user: User) -> None:
        return None

    def collect_challenges(self, user: User) -> None:
        return None

    def collect_latest_job_postings(self, user: User) -> None:
        return None

    def collect_latest_challenges(self, user: User) -> None:
        return None

    def collect_requested_matches(self, user: User) -> None:
        return None

    def collect_unconfirmed_matches(self, user: User) -> None:
        return None

    def collect_confirmed_matches(self, user: User) -> None:
        return None

    def collect_challenge_matches(self, user: User) -> None:
        return None
