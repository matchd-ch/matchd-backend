from abc import ABC

from db.models.user import User


class DashboardData(ABC):

    def __init__(self, user: User) -> None:
        self._data = {
            'job_postings': self.collect_job_postings(user),
            'project_postings': self.collect_project_postings(user),
            'latest_job_postings': self.collect_latest_job_postings(user),
            'latest_project_postings': self.collect_latest_project_postings(user),
            'requested_matches': self.collect_requested_matches(user),
            'unconfirmed_matches': self.collect_unconfirmed_matches(user),
            'confirmed_matches': self.collect_confirmed_matches(user),
            'project_matches': self.collect_project_matches(user),
        }

    @property
    def data(self) -> dict:
        return self._data

    def collect_job_postings(self, user: User) -> None:
        return None

    def collect_project_postings(self, user: User) -> None:
        return None

    def collect_latest_job_postings(self, user: User) -> None:
        return None

    def collect_latest_project_postings(self, user: User) -> None:
        return None

    def collect_requested_matches(self, user: User) -> None:
        return None

    def collect_unconfirmed_matches(self, user: User) -> None:
        return None

    def collect_confirmed_matches(self, user: User) -> None:
        return None

    def collect_project_matches(self, user: User) -> None:
        return None
