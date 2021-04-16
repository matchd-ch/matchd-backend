from api.helper import is_me_query
from db.models import Student, ProfileState


def privacy(func):
    def wrapper(self: Student, info):
        if self.state != ProfileState.PUBLIC:
            if is_me_query(info):
                return func(self, info)
            return None
        return func(self, info)
    return wrapper
