from db.models import UserState, UserType


def has_access_to_attachments(user, owner):
    # check if user has a public profile, or the user is the owner of the attachments
    has_access = False
    if user.id == owner.id:
        has_access = True
    else:
        # show attachments for all companies
        user_type = owner.type
        # check if the user has a public profile
        state = owner.state

        if user_type in UserType.valid_company_types():
            if state != UserState.INCOMPLETE:
                has_access = True
        else:
            if state == UserState.PUBLIC:
                has_access = True
    return has_access
