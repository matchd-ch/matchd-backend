from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from db.models import ProfileType


class MatchType(models.TextChoices):
    STUDENT = 'student', _('Student')
    JOB_POSTING = 'job_posting', _('Job posting')


class Match(models.Model):
    student = models.ForeignKey('db.Student', null=False, on_delete=models.CASCADE)
    job_posting = models.ForeignKey('db.JobPosting', null=False, on_delete=models.CASCADE)
    student_confirmed = models.BooleanField(default=False)
    company_confirmed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_confirmed = models.DateTimeField(null=True)
    initiator = models.CharField(choices=ProfileType.choices, max_length=100)
    complete = models.BooleanField(default=False)

    def send_email(self):
        template = 'company'
        recipients = [self.student.user.email]
        url_link = f'{settings.FRONTEND_URL_PROTOCOL}{settings.PROFILE_URL_STUDENT}{self.student.slug}'
        if self.initiator == ProfileType.STUDENT:
            template = 'student'
            recipients = [self.job_posting.employee.user.email]
            url_link = f'{settings.FRONTEND_URL_PROTOCOL}{settings.PROFILE_URL_COMPANY}{self.job_posting.company.slug}'

        email_context = {
            'company': self.job_posting.company,
            'url_link': url_link,
            'student': self.student.user,
            'job_posting': self.job_posting
        }

        subject = render_to_string(f'db/email/match/{template}/start_match.subject.txt', email_context)
        plain_body = render_to_string(f'db/email/match/{template}/start_match.body_plain.txt', email_context)
        html_body = render_to_string(f'db/email/match/{template}/start_match.body.html', email_context)
        send_mail(
            subject,
            plain_body,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            html_message=html_body
        )
