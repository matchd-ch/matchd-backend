from django.contrib.auth import get_user_model
from django.utils.text import slugify
from graphql_auth.models import UserStatus

from db.models import DateMode, JobType
from db.seed.base import BaseSeed


# pylint: disable=W0612
class User(BaseSeed):

    def create_or_update(self, data, *args, **kwargs):
        email = data.get('email')
        user, created = get_user_model().objects.get_or_create(email=email)
        user.username = email
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.type = data.get('type')
        user.set_password('asdf1234$')
        user.save()
        user_status, created = UserStatus.objects.get_or_create(user=user)
        user_status.verified = data.get('verified')
        user_status.save()
        return user

    def random(self, *args, **kwargs):
        i = kwargs.get('index')
        email = f"dummy-student-{str(i)}@matchd.localhost"
        gender = self.rand.gender()
        languages = self.rand.languages()
        name = self.rand.name(gender)
        nickname = f'{slugify(name)}-{str(i)}'
        first_name, last_name = name.split(' ')
        street, zip_value, city = self.rand.address()
        avatar = self.rand.avatar(gender)
        job_type = self.rand.job_type()
        job_type_object = JobType.objects.get(pk=job_type)
        job_from_date = self.rand.job_from_date()
        job_to_date = None
        if job_type_object.mode == DateMode.DATE_RANGE:
            job_to_date = self.rand.job_to_date(job_from_date)

        attachments = [{
            "file": f'avatars/{gender}/{avatar}',
            "key": "student_avatar",
            "type": "db.image",
            "user": email
        }]
        documents = self.rand.documents()
        for document in documents:
            attachments.append({
                "file": f'documents/{document}',
                "key": "student_documents",
                "type": "db.file",
                "user": email
            })

        dummy = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "student": {
                "attachments": attachments,
                "branch": self.rand.branch(),
                "city": city,
                "cultural_fits": self.rand.cultural_fits(),
                "date_of_birth": self.rand.date_of_birth(),
                "distinction": self.rand.distinction(),
                "field_of_study": "Studiengang",
                "graduation": self.rand.graduation(),
                "hobbies": self.rand.hobbies(),
                "job_from_date": job_from_date,
                "job_to_date": job_to_date,
                "job_type": job_type,
                "languages": languages,
                "mobile": self.rand.mobile(),
                "nickname": nickname,
                "slug": slugify(nickname),
                "online_challenges": self.rand.online_challenges(),
                "profile_step": 7,
                "school_name": "School name",
                "skills": self.rand.skills(),
                "soft_skills": self.rand.soft_skills(),
                "state": self.rand.state(),
                "street": street,
                "zip": zip_value
            },
            "type": "student",
            "verified": 1
        }
        return dummy
