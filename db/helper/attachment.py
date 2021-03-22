from db.models import ProfileState


def has_access_to_attachments(user, owner):
    # owner can be a user or a company
    # check if user has a public profile, or the user is the owner of the attachments
    owner_is_company = True
    if hasattr(owner, 'username'):
        owner_is_company = False

    has_access = False

    if owner_is_company:
        # company
        company_users = owner.users.all()
        if user in company_users:
            has_access = True
        else:
            # check if the company has a completed profile
            state = company_users[0].state
            if state != ProfileState.INCOMPLETE:
                has_access = True
    else:
        # user
        if user.id == owner.id:
            has_access = True
        else:
            # check if the user has a public profile
            state = owner.state
            if state == ProfileState.PUBLIC:
                has_access = True

    return has_access
