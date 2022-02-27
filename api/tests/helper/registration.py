from django.conf import settings


def verify_notification_new_user(user, notification_email):
    assert settings.EMAIL_SYSTEM_NOTIFICATION_PREFIX in notification_email.subject
    assert 'New user registration' in notification_email.subject

    assert f'First name: {user.first_name}' in notification_email.body
    assert f'Last name: {user.last_name}' in notification_email.body
    assert f'Email: {user.email}' in notification_email.body
    assert f'Type: {user.type}' in notification_email.body
    assert f'Company: {user.company}' in notification_email.body