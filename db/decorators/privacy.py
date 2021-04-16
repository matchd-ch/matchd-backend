from db.models import Student, ProfileState


def privacy(func):
    def wrapper(self: Student, obj):
        if self.state != ProfileState.PUBLIC:
            return None
        return func(self, obj)
    return wrapper
