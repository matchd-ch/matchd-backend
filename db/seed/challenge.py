from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from db.models import ProfileState, Challenge as ChallengeModel, ChallengeState
from db.seed.base import BaseSeed


# pylint: disable=W0612
# pylint: disable=R0912
# pylint: disable=R0915
# pylint: disable=R1710
class Challenge(BaseSeed):

    def create_or_update(self, data, *args, **kwargs):
        if data is None:
            return

        if data.get('company') is not None and len(data.get('company').keys()) == 1:
            return

        company = kwargs.get('company')
        challenges = None
        if company is not None:
            if company.state == ProfileState.INCOMPLETE:
                return
            challenges = data.get('company').get('challenges')
        student = kwargs.get('student')
        if student is not None:
            if student.state == ProfileState.INCOMPLETE:
                return
            challenges = data.get('student').get('challenges')

        employee = kwargs.get('employee')
        student = kwargs.get('student')
        company = kwargs.get('company')

        result = []

        if challenges is None or len(challenges) == 0:
            for i in range(0, self.rand.number()):

                challenge = ChallengeModel(title=self.rand.challenge_title(),
                                           description=self.rand.description(),
                                           challenge_type_id=self.rand.challenge_type(),
                                           challenge_from_date=self.rand.challenge_from_date(),
                                           team_size=5,
                                           compensation="To be discussed",
                                           website='https://www.challenge.lo',
                                           form_step=3,
                                           state=self.rand.challenge_state(),
                                           employee=employee,
                                           company=company,
                                           student=student)
                challenge.save()
                if challenge.state == ChallengeState.PUBLIC:
                    challenge.date_published = challenge.date_created
                challenge.slug = f'{slugify(challenge.title)}-{str(challenge.id)}'
                challenge.save()
                challenge.keywords.set(self.rand.keywords())
                result.append(challenge)
        else:
            for obj in challenges:
                try:
                    challenge = ChallengeModel.objects.get(slug=obj.get('slug'))
                except ChallengeModel.DoesNotExist:
                    challenge = ChallengeModel(challenge_type_id=obj.get('challenge_type'),
                                               company=company,
                                               employee=employee,
                                               student=student)
                challenge_title = obj.get('title', None)
                if challenge_title is None:
                    challenge_title = self.rand.title()
                challenge.title = challenge_title
                challenge.description = obj.get('description')
                challenge.website = obj.get('website')
                date_created = obj.get('date_created')
                date_created = datetime.strptime(
                    date_created,
                    '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
                date_published = obj.get('date_published')
                if date_published is not None:
                    date_published = datetime.strptime(
                        date_published,
                        '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
                challenge.date_created = date_created
                challenge.date_published = date_published
                if challenge.state == ChallengeState.PUBLIC and challenge.date_created is None:
                    challenge.date_published = challenge.date_created
                challenge.challenge_from_date = obj.get('challenge_from_date')
                challenge.form_step = obj.get('form_step')
                challenge.state = obj.get('state')
                challenge.team_size = 5
                challenge.compensation = "To be discussed"
                employee = None
                if obj.get('employee') is not None:
                    employee = get_user_model().objects.get(email=obj.get('employee')).employee
                challenge.employee = employee
                challenge.save()
                slug = obj.get('slug')
                if slug is None or slug == '':
                    slug = f'{slugify(challenge.title)}-{str(challenge.id)}'
                challenge.slug = slug
                challenge.save()
                challenge.keywords.set(obj.get('keywords'))
                result.append(challenge)
        return result

    def random(self, *args, **kwargs):
        pass
