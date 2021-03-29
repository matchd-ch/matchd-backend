from db.models import ProfileState, ProfileType


def has_access_to_attachments(user, owner):
    # check if user has a public profile, or the user is the owner of the attachments
    owner_is_company = True
    if owner.type != ProfileType.COMPANY:
        owner_is_company = False

    has_access = False

    if owner_is_company:
        # company
        company_users = owner.company.users.all()
        if user in company_users:
            has_access = True
        else:
            # check if the company has a completed profile
            # company attachment are accessible for anonymous and public profile
            state = owner.company.state
            if state != ProfileState.INCOMPLETE:
                has_access = True
    else:
        # user
        if user.id == owner.id:
            has_access = True
        else:
            # check if the user has a public profile
            state = owner.student.state
            if state == ProfileState.PUBLIC:
                has_access = True

    return has_access
