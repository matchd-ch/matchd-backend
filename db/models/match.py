from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from .profile_type import ProfileType


class MatchType(models.TextChoices):
    STUDENT = 'student', _('Student')
    JOB_POSTING = 'job_posting', _('Job posting')
    PROJECT_POSTING = 'project_posting', _('Project posting')
    COMPANY = 'company', _('Company')
    UNIVERSITY = 'university', _('University')


class Match(models.Model):
    student = models.ForeignKey('db.Student', null=True, on_delete=models.CASCADE)
    job_posting = models.ForeignKey('db.JobPosting', null=True, on_delete=models.CASCADE)
    project_posting = models.ForeignKey('db.ProjectPosting', null=True, on_delete=models.CASCADE)
    company = models.ForeignKey('db.Company', null=True, on_delete=models.CASCADE)
    student_confirmed = models.BooleanField(default=False)
    company_confirmed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_confirmed = models.DateTimeField(null=True)
    initiator = models.CharField(choices=ProfileType.choices, max_length=100)
    complete_mail_sent = models.BooleanField(default=False)

    @property
    def complete(self):
        return self.student_confirmed and self.company_confirmed

    def send_complete_job_match_mail(self):
        email_context = self._email_context()
        template_path = 'db/email/match/student/'

        # email student
        recipients = [self.student.user.email]
        subject = render_to_string(f'{template_path}complete_match.subject.txt', email_context)
        plain_body = render_to_string(f'{template_path}complete_match.body_plain.txt', email_context)
        html_body = render_to_string(f'{template_path}complete_match.body.html', email_context)
        send_mail(
            subject,
            plain_body,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            html_message=html_body
        )

        # email company
        template_path = 'db/email/match/company/'
        recipients = [self.job_posting.employee.user.email]
        subject = render_to_string(f'{template_path}complete_match.subject.txt', email_context)
        plain_body = render_to_string(f'{template_path}complete_match.body_plain.txt', email_context)
        html_body = render_to_string(f'{template_path}complete_match.body.html', email_context)
        send_mail(
            subject,
            plain_body,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            html_message=html_body
        )

    def send_start_job_match_email(self):
        if self.initiator == ProfileType.COMPANY:
            self._send_initiator_company()

        if self.initiator in ProfileType.valid_student_types():
            self._send_initiator_student()

    def _student_profile_url(self):
        return f'{settings.FRONTEND_URL_PROTOCOL}{settings.FRONTEND_URL}{settings.STUDENT_PROFILE_URL}' \
               f'{self.student.slug}?jobPostingId={self.job_posting.id}'

    def _job_posting_url(self):
        return f'{settings.FRONTEND_URL_PROTOCOL}{settings.FRONTEND_URL}{settings.JOB_POSTING_URL}' \
               f'{self.job_posting.slug}'

    def _email_context(self):
        return {
            'company': self.job_posting.company,
            'student': self.student.user,
            'job_posting_url': self._job_posting_url(),
            'job_posting': self.job_posting,
            'student_profile_url': self._student_profile_url(),
            'email_subject_prefix': settings.EMAIL_SUBJECT_PREFIX,
        }

    def _send_initiator_company(self):
        email_context = self._email_context()
        template_path = 'db/email/match/student/'

        # email student
        recipients = [self.student.user.email]
        subject = render_to_string(f'{template_path}start_match.subject.txt', email_context)
        plain_body = render_to_string(f'{template_path}start_match.body_plain.txt', email_context)
        html_body = render_to_string(f'{template_path}start_match.body.html', email_context)
        send_mail(
            subject,
            plain_body,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            html_message=html_body
        )

        # email company
        recipients = [self.job_posting.employee.user.email]
        subject = render_to_string(f'{template_path}copy.start_match.subject.txt', email_context)
        plain_body = render_to_string(f'{template_path}copy.start_match.body_plain.txt', email_context)
        html_body = render_to_string(f'{template_path}copy.start_match.body.html', email_context)
        send_mail(
            subject,
            plain_body,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            html_message=html_body
        )

    def _send_initiator_student(self):
        email_context = self._email_context()
        template_path = 'db/email/match/company/'

        # email company
        recipients = [self.job_posting.employee.user.email]
        subject = render_to_string(f'{template_path}start_match.subject.txt', email_context)
        plain_body = render_to_string(f'{template_path}start_match.body_plain.txt', email_context)
        html_body = render_to_string(f'{template_path}start_match.body.html', email_context)
        send_mail(
            subject,
            plain_body,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            html_message=html_body
        )

        # email student
        recipients = [self.student.user.email]
        subject = render_to_string(f'{template_path}copy.start_match.subject.txt', email_context)
        plain_body = render_to_string(f'{template_path}copy.start_match.body_plain.txt', email_context)
        html_body = render_to_string(f'{template_path}copy.start_match.body.html', email_context)
        send_mail(
            subject,
            plain_body,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            html_message=html_body
        )

    def send_complete_project_match_mail(self):
        email_context = self._email_context()
        template_path = 'db/email/project/'

        # email student
        recipients = [self.student.user.email]
        subject = render_to_string(f'{template_path}match.subject.txt', email_context)
        plain_body = render_to_string(f'{template_path}match.body_plain.txt', email_context)
        html_body = render_to_string(f'{template_path}match.body.html', email_context)
        send_mail(
            subject,
            plain_body,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            html_message=html_body
        )

        # email company
        recipients = [self.job_posting.employee.user.email]
        subject = render_to_string(f'{template_path}match.subject.txt', email_context)
        plain_body = render_to_string(f'{template_path}match.body_plain.txt', email_context)
        html_body = render_to_string(f'{template_path}match.body.html', email_context)
        send_mail(
            subject,
            plain_body,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            html_message=html_body
        )

