from django.conf import settings
from django.core.mail import mail_managers
from django.template.loader import render_to_string
from django.utils.translation import gettext as _


def notify_managers_new_user_registration(user):
    email_context = {
        'subject': _("New user registration"),
        'user': user,
        'email_system_notification_subject_prefix': settings.EMAIL_SYSTEM_NOTIFICATION_PREFIX,
    }

    subject = render_to_string('db/email/notification/internal/registration/user/new.subject.txt',
                               email_context)
    plain_body = render_to_string('db/email/notification/internal/registration/user/new.plain.txt',
                                  email_context)

    mail_managers(subject, plain_body)
