import random

from django.conf import settings
from django.urls import reverse

from db.models import ProfileState, Student, ProfileType, Match, AttachmentKey


def has_access_to_attachments(user, owner, key=None):
    # this could happen if the owner is an internal user (eg. ProfileType.INTERNAL). See get_company_or_student()
    if owner is None:
        return False
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

            # students should not have access to other students attachments
            if user.type not in ProfileType.valid_company_types():
                has_access = False
            elif key is None:
                # this should not happen
                has_access = False
            elif key == AttachmentKey.STUDENT_DOCUMENTS:
                # allow access only if a confirmed match exists (only confirmed by student)
                match_exists = Match.objects.filter(student=owner, job_posting__company=user.company,
                                                    student_confirmed=True).exists()
                has_access = match_exists
            elif state == ProfileState.PUBLIC:
                has_access = True
    return has_access


def get_company_or_student(user):
    if user.type in ProfileType.valid_company_types():
        return user.company
    if user.type in ProfileType.valid_student_types():
        return user.student
    return None


def get_fallback_profile_image():
    random_id = random.randint(1, settings.NUMBER_OF_RANDOM_PROFILE_IMAGES)
    path = reverse('media_serve_image', args=[random_id, '--STACK--'])
    path = path.replace('--STACK--', '{stack}')  # Workaround to avoid URL escaping
    return f'{settings.BASE_URL}{path}'
