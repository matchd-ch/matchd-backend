from db.models.challenge import Challenge


def hide_challenge_attributes(challenge):
    challenge.team_size = None
    challenge.compensation = None
    challenge.website = ""
    challenge.employee = None
    challenge.student = None
    challenge.company = None
    challenge.match_status = None
    challenge.match_hints = None
    challenge.form_step = 0

    return challenge


def restrict_challenge(func):

    def wrapper(self, info, **kwargs):
        result = func(self, info, **kwargs)

        if info.context.user is None or not info.context.user.is_authenticated:
            if isinstance(result, Challenge):
                result = hide_challenge_attributes(result)
            else:
                result = list(map(hide_challenge_attributes, result))

        return result

    return wrapper


def restrict_challenge_node(func):

    def wrapper(self, info, node_id):
        result = func(self, info, node_id)

        if info.context.user is None or not info.context.user.is_authenticated:
            if isinstance(result, Challenge):
                result = hide_challenge_attributes(result)
            else:
                result = None

        return result

    return wrapper
