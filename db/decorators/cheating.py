from api.helper import is_me_query
from db.models import ProfileType, JobPosting


def cheating_protection(func):
    def wrapper(self, info):
        user = info.context.user
        if not user.is_anonymous and user.type in ProfileType.valid_company_types():
            compare_company = self
            if isinstance(self, JobPosting):
                compare_company = self.company
            if user.company == compare_company:
                return func(self, info)
        if is_me_query(info):
            return func(self, info)
        return None
    return wrapper
