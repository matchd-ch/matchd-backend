from api.helper import is_me_query
from db.models import Student, ProfileState, ProfileType


def privacy_protection(match_only=False):
    def decorator(func):
        def wrapper(self: Student, info):
            if is_me_query(info):
                return func(self, info)

            # check for possible matches
            user = info.context.user
            if not user.is_anonymous and user.type in ProfileType.valid_company_types():
                if self.has_match(user.company):
                    return func(self, info)

            # get out, if a match is required for this value
            if match_only:
                return None
            if self.state == ProfileState.PUBLIC:
                return func(self, info)
            return None
        return wrapper
    return decorator
