from db.models import ProfileState, Student, ProfileType


def has_access_to_attachments(user, owner):
    # owner is an instance of company or student
    # check if user has a public profile, or the user is the owner of the attachments
    owner_is_company = True
    if isinstance(owner, Student):
        owner_is_company = False
    has_access = False

    if owner_is_company:
        # company
        company_users = owner.users.all()
        if user in company_users:
            has_access = True
        else:
            # check if the company has a completed profile
            # company attachment are accessible for anonymous and public profile
            state = owner.state
            if state != ProfileState.INCOMPLETE:
                has_access = True
    else:
        # user
        if user.id == owner.user.id:
            has_access = True
        else:
            # check if the user has a public profile
            state = owner.state
            if state == ProfileState.PUBLIC:
                has_access = True

    return has_access


def get_company_or_student(user):
    if user.type in ProfileType.valid_company_types():
        return user.company
    return user.student
