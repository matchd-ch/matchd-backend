from api.helper import is_me_query


def cheating_protection(func):
    def wrapper(self, info):
        if is_me_query(info):
            return func(self, info)
        return None
    return wrapper
