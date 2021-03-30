import json

from django.contrib.auth import get_user_model
from graphql_auth.models import UserStatus

from db.helper.forms import convert_date
from db.models import ProfileType, Student as StudentModel


class Student:

    users = None

    def run(self):
        self.read_users()
        index = 1
        for user in self.users:
            self.create_student(user, index)
            index += 1

    def read_users(self):
        with open('db/management/seed/students.json') as json_file:
            self.users = json.load(json_file)

    def create_student(self, user_data, index):
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        username = 'student-%s@matchd.lo' % str(index)

        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            user = user_model.objects.create(
                username=username,
                email=username,
                is_staff=False,
                is_active=True,
                is_superuser=False,
                type=ProfileType.STUDENT,
                first_name=first_name,
                last_name=last_name
            )

        user.set_password('asdf1234$')
        user.save()

        try:
            UserStatus.objects.get(user=user)
        except UserStatus.DoesNotExist:
            UserStatus.objects.create(
                user=user,
                verified=True,
                archived=False
            )

        try:
            student = StudentModel.objects.get(user=user)
        except StudentModel.DoesNotExist:
            student = StudentModel.objects.create(user=user)

        student.mobile = user_data.get('mobile')
        student.street = user_data.get('street')
        student.zip = user_data.get('street')
        student.city = user_data.get('city')
        student.date_of_birth = convert_date(user_data.get('date_of_birth'), '%d.%m.%Y')
        student.nickname = user_data.get('nickname')
        student.school_name = user_data.get('school_name')
        student.field_of_study = user_data.get('field_of_study')
        student.graduation = convert_date(user_data.get('graduation'), '%m.%Y')
        student.job_option = user_data.get('job_option')
        student.job_from_date = user_data.get('job_from_date')
        student.job_to_date = user_data.get('job_to_date')
        student.job_position = user_data.get('job_position')
        student.skills.set(user_data.get('skills'))
        student.distinction = user_data.get('distinction')
        student.state = user_data.get('state')
        student.profile_step = user_data.get('profile_step')
        student.soft_skills.set(user_data.get('soft_skills'))
        student.save()

        return user
