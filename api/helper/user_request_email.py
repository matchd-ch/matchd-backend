from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_user_request_email(user_request, context):
    _send_email(user_request, 'user_request_copy', [user_request.email], context)
    _send_email(user_request, 'user_request', settings.USER_REQUEST_FORM_RECIPIENTS, context)


def _send_email(user_request, email_type, recipients, context):
    email_context = {
        'name': user_request.name,
        'email': user_request.email,
        'message': user_request.message,
        'email_subject_prefix': settings.EMAIL_SUBJECT_PREFIX,
    }
    subject = render_to_string(f'db/email/{email_type}/subject.txt', email_context, context)
    plain_body = render_to_string(f'db/email/{email_type}/body_plain.txt', email_context, context)
    html_body = render_to_string(f'db/email/{email_type}/body.html', email_context, context)
    send_mail(subject, plain_body, settings.DEFAULT_FROM_EMAIL, recipients, html_message=html_body)
