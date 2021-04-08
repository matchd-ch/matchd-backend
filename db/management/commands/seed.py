import json
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from graphql_auth.models import UserStatus

from db.models import Employee, Student, Hobby, OnlineProject, UserLanguageRelation, CulturalFit, Skill, SoftSkill, \
    Branch, JobType, ProfileState, Language, LanguageLevel


class Command(BaseCommand):
    help = 'Generates test data'
    data = []

    random_hobbies = [
        'Gamen', 'Fussball', 'Programmieren', 'Kochen', 'Jodeln', 'Wandern', 'Handball', 'Lego', 'Gitarre', 'Flöte',
        'mit dem Hund spazieren', 'Kollegen treffen', 'Ausgang', 'Bowling', 'Malen', 'Zeichnen'
    ]

    random_cultural_fits = []
    random_skills = []
    random_soft_skills = []
    random_branches = []
    random_job_types = []
    random_languages = []
    random_language_levels = []

    def load_data(self):
        with open('db/management/seed/fixtures.json') as json_file:
            self.data = json.load(json_file)

        self.random_cultural_fits = list(CulturalFit.objects.all().values_list('id', flat=True))
        self.random_skills = list(Skill.objects.all().values_list('id', flat=True))
        self.random_soft_skills = list(SoftSkill.objects.all().values_list('id', flat=True))
        self.random_branches = list(Branch.objects.all().values_list('id', flat=True))
        self.random_job_types = list(JobType.objects.all().values_list('id', flat=True))
        self.random_languages = list(Language.objects.all().values_list('id', flat=True))
        self.random_language_levels = list(LanguageLevel.objects.all().values_list('id', flat=True))

    def random_items(self, items, count):
        random.shuffle(items)
        if count == 1:
            return items[0]
        return items[:count]

    # noinspection PyUnresolvedReferences
    def handle(self, *args, **options):
        self.load_data()
        self.stdout.write('Adding test data...')

        # create users first
        for user_data in self.data:
            user = self.create_user(user_data)
            self.create_employee(user, user_data.get('employee'))
            self.create_student(user, user_data.get('student'))

        self.stdout.write(self.style.SUCCESS('Adding test data completed'))

    def create_user(self, data):
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

    def create_employee(self, user, data):
        if data is None:
            return

        employee, created = Employee.objects.get_or_create(user=user)
        employee.role = data.get('role')
        employee.save()

    def create_student(self, user, data):
        if data is None:
            return
        student, created = Student.objects.get_or_create(user=user)
        is_complete = user.student.state != ProfileState.INCOMPLETE

        branch = data.get('branch')
        if branch is None and is_complete:
            student.branch_id = self.random_items(self.random_branches, 1)
        else:
            student.branch_id = branch
        student.city = data.get('city')
        cultural_fits = data.get('cultural_fits')
        if len(cultural_fits) == 0 and is_complete:
            student.cultural_fits.set(self.random_items(self.random_cultural_fits, 6))
        else:
            student.cultural_fits.set(cultural_fits)
        student.date_of_birth = data.get('date_of_birth')
        student.distinction = data.get('distinction')
        student.field_of_study = data.get('field_of_study')
        student.graduation = data.get('graduation')
        hobbies = data.get('hobbies')
        if len(data.get('hobbies')) == 0 and is_complete:
            for hobby in self.random_items(self.random_hobbies, 3):
                Hobby.objects.get_or_create(student=student, name=hobby)
        else:
            for hobby in hobbies:
                Hobby.objects.get_or_create(student=student, name=hobby)

        student.job_from_date = data.get('job_from_date')
        student.job_to_date = data.get('job_to_date')
        job_type = data.get('job_type')
        if job_type is None and is_complete:
            student.job_type_id = self.random_items(self.random_job_types, 1)
        else:
            student.job_type_id = job_type

        languages = data.get('languages')
        if len(languages) == 0 and is_complete:
            random_languages = self.random_items(self.random_languages, 3)
            random_language_levels = self.random_items(self.random_language_levels, 3)
            index = 0
            for language in random_languages:
                UserLanguageRelation.objects.create(student=student, language_id=language,
                                                    language_level_id=random_language_levels[index])
                index += 1
        else:
            for language in languages:
                UserLanguageRelation.objects.get_or_create(student=student, language_id=language.get('language'),
                                                           language_level_id=language.get('language_level'))
        student.mobile = data.get('mobile')
        student.nickname = data.get('nickname')
        online_projects = data.get('online_projects')
        if len(online_projects) == 0 and is_complete:
            OnlineProject.objects.create(student=student, url='http://www.project.lo')
            OnlineProject.objects.create(student=student, url='http://www.project2.lo')
        else:
            for online_project in online_projects:
                OnlineProject.objects.get_or_create(student=student, url=online_project)
        student.profile_step = data.get('profile_step')
        student.school_name = data.get('school_name')

        skills = data.get('skills')
        if len(skills) == 0 and is_complete:
            student.skills.set(self.random_items(self.random_skills, 4))
        else:
            student.skills.set(skills)

        soft_skills = data.get('soft_skills')
        if len(skills) == 0 and is_complete:
            student.soft_skills.set(self.random_items(self.random_soft_skills, 4))
        else:
            student.soft_skills.set(soft_skills)

        student.state = data.get('state')
        student.zip = data.get('street')
        student.save()

