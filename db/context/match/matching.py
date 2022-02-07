from abc import ABC, abstractmethod

from db.models.user import User


class Matching(ABC):

    def __init__(self, user: User, **kwargs: dict) -> None:
        self._user = self.collect_user(user)
        self._data = self.collect_data(**kwargs)
        self._first = self.collect_first(**kwargs)
        self._skip = self.collect_skip(**kwargs)
        self._tech_boost = self.collect_tech_boost(**kwargs)
        self._soft_boost = self.collect_soft_boost(**kwargs)

    @abstractmethod
    def _validate_input(self):
        pass

    @abstractmethod
    def find_matches(self):
        pass

    def collect_user(self, user):
        return user

    def collect_data(self, **kwargs: dict):
        return kwargs.get('data')

    def collect_first(self, **kwargs: dict) -> str:
        return kwargs.get('first')

    def collect_skip(self, **kwargs: dict) -> str:
        return kwargs.get('skip')

    def collect_tech_boost(self, **kwargs: dict) -> int:
        return max(min(kwargs.get('tech_boost', 1), 5), 1)

    def collect_soft_boost(self, **kwargs: dict) -> int:
        return max(min(kwargs.get('soft_boost', 1), 5), 1)

    @property
    def user(self):
        return self._user

    @property
    def data(self):
        return self._data

    @property
    def first(self):
        return self._first

    @property
    def skip(self):
        return self._skip

    @property
    def tech_boost(self):
        return self._tech_boost

    @property
    def soft_boost(self):
        return self._soft_boost
