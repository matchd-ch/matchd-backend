from api.helper import is_me_query
from db.models import Student, ProfileState


def privacy(func):
    def wrapper(self: Student, info):
        if is_me_query(info):
            return func(self, info)
        if self.state == ProfileState.PUBLIC:
            return func(self, info)
        return None
    return wrapper
