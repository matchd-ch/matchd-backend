from api.helper import is_me_query
from db.models import ProfileType


def job_posting_cheating_protection(func):
    def wrapper(self, info):
        user = info.context.user
        if user.company == self.company:
            return func(self, info)
        if is_me_query(info):
            return func(self, info)
        return None
    return wrapper


def company_cheating_protection(func):
    def wrapper(self, info):
        user = info.context.user
        if not user.is_anonymous and user.type in ProfileType.valid_company_types():
            if user.company == self:
                return func(self, info)
        if is_me_query(info):
            return func(self, info)
        return None
    return wrapper
