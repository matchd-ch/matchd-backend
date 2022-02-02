from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.template.loader import render_to_string


class UserRequest(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    message = models.TextField(max_length=1024, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        is_raw = kwargs.get('raw', False)
        post_save.disconnect(UserRequest.post_save,
                             UserRequest,
                             dispatch_uid='db.models.UserRequest')
        if created and not is_raw:
            instance.send_email('user_request_copy', [instance.email])
            instance.send_email('user_request', settings.USER_REQUEST_FORM_RECIPIENTS)
        post_save.connect(UserRequest.post_save, UserRequest, dispatch_uid='db.models.UserRequest')

    def send_email(self, email_type, recipients):
        email_context = {
            'name': self.name,
            'email': self.email,
            'message': self.message,
            'email_subject_prefix': settings.EMAIL_SUBJECT_PREFIX,
        }
        subject = render_to_string(f'db/email/{email_type}/subject.txt', email_context)
        plain_body = render_to_string(f'db/email/{email_type}/body_plain.txt', email_context)
        html_body = render_to_string(f'db/email/{email_type}/body.html', email_context)
        send_mail(subject,
                  plain_body,
                  settings.DEFAULT_FROM_EMAIL,
                  recipients,
                  html_message=html_body)


post_save.connect(UserRequest.post_save, UserRequest, dispatch_uid='db.models.UserRequest')
