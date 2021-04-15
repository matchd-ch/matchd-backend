from datetime import datetime, timedelta
import os
import random

import names
from dateutil.relativedelta import relativedelta
from django.conf import settings

from db.models import Branch, CulturalFit, JobType, Language, LanguageLevel, Skill, SoftSkill, ProfileState, Benefit, \
    JobRequirement


class Random:

    def __init__(self):
        self._gender_data = ['male', 'female']
        path = os.path.join(settings.MEDIA_ROOT, 'student_fixtures', 'avatars', 'male')
        self._male_avatars = self._load_files(path)
        path = os.path.join(settings.MEDIA_ROOT, 'student_fixtures', 'avatars', 'female')
        self._female_avatars = self._load_files(path)
        path = os.path.join(settings.MEDIA_ROOT, 'student_fixtures', 'documents')
        self._documents = self._load_files(path)
        path = os.path.join(settings.MEDIA_ROOT, 'company_fixtures', 'moods')
        self._moods = self._load_files(path)
        path = os.path.join(settings.MEDIA_ROOT, 'company_fixtures', 'avatars')
        self._logos = self._load_files(path)

        self._branches = list(Branch.objects.all().values_list('id', flat=True))
        self._cultural_fits = list(CulturalFit.objects.all().values_list('id', flat=True))
        self._job_types = list(JobType.objects.all().values_list('id', flat=True))
        self._languages = list(Language.objects.all().values_list('id', flat=True))
        self._language_levels = list(LanguageLevel.objects.all().values_list('id', flat=True))
        self._skills = list(Skill.objects.all().values_list('id', flat=True))
        self._soft_skills = list(SoftSkill.objects.all().values_list('id', flat=True))
        self._benefits = list(Benefit.objects.all().values_list('id', flat=True))
        self._requirements = list(JobRequirement.objects.all().values_list('id', flat=True))

        self._addresses = self._load_address_data()
        self._hobby_data = [
            'Gamen', 'Fussball', 'Programmieren', 'Kochen', 'Jodeln', 'Wandern', 'Handball', 'Lego', 'Gitarre', 'Flöte',
            'mit dem Hund spazieren', 'Kollegen treffen', 'Ausgang', 'Bowling', 'Malen', 'Zeichnen'
        ]
        self._state_data = [ProfileState.PUBLIC, ProfileState.ANONYMOUS]

        self._titles = [
            'Praktikant*in Applikationsentwicklung', 'Praktikant*in Systemtechnik', 'Praktikant*in DevOps',
            'Praktikant*in Frontendentwicklung', 'Praktikant*in HTML / CSS', 'Praktikant*in Design', 'Praktikant*in UX',
            'Praktikant*in Grafik', 'Praktikant*in User Experience', 'Praktikant*in Social Media',
            'Praktikant*in Datenbanken', 'Praktikant*in PHP', 'Praktikant*in Python', 'Praktikant*in Javascript',
            'Praktikant*in Vue.js / React.js'
        ]
        self._workloads = [50, 60, 70, 80, 90, 100]

    def _random(self, items, count):
        random.shuffle(items)
        if count == 1:
            return items[0]
        return items[:count]

    def _load_files(self, path):
        path = os.path.join(settings.MEDIA_ROOT, path)
        file_names = [
            file_name for file_name in os.listdir(path) if os.path.isfile(os.path.join(path, file_name))
        ]
        files = []
        for file_name in file_names:
            if file_name[0] == '.':
                continue
            files.append(file_name)
        return files

    def _load_address_data(self):
        address_list = []
        with open('db/seed/data/address_list.txt') as address_file:
            lines = address_file.readlines()
            for line in lines:
                parts = line.split(',')
                address = parts[0].strip()
                parts2 = parts[1].split(' - ')
                address_list.append(
                    (address, parts2[0].strip(), parts2[1].strip())
                )
        return address_list

    def _date(self, date):
        return datetime.strptime(date, '%Y-%m-%d').date()

    def _date_between(self, start, end):
        start = self._date(start)
        end = self._date(end)
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return start + timedelta(seconds=random_second)

    def _has_german(self, languages):
        for language in languages:
            if language == 5:
                return True
        return False

    def gender(self):
        return self._random(self._gender_data, 1)

    def name(self, gender):
        return names.get_full_name(gender=gender)

    def avatar(self, gender):
        if gender == 'male':
            return self._random(self._male_avatars, 1)
        return self._random(self._female_avatars, 1)

    def branch(self):
        return self._random(self._branches, 1)

    def branches(self):
        count = random.randint(2, 5)
        return self._random(self._branches, count)

    def address(self):
        return self._random(self._addresses, 1)

    def cultural_fits(self):
        return self._random(self._cultural_fits, 6)

    def date_of_birth(self):
        return self._date_between('1978-01-01', '2005-12-31')

    def hobbies(self):
        count = random.randint(2, 5)
        return self._random(self._hobby_data, count)

    def job_type(self):
        return self._random(self._job_types, 1)

    def job_from_date(self):
        return self._date_between('2020-01-01', '2021-12-21')

    def job_to_date(self, from_date):
        end_date = from_date + relativedelta(months=12)
        return self._date_between(datetime.strftime(from_date, '%Y-%m-%d'), datetime.strftime(end_date, '%Y-%m-%d'))

    def languages(self):
        languages = self._random(self._languages, 3)
        if not self._has_german(languages):
            languages.append(5)  # german
        levels = self._random(self._language_levels, len(languages))
        result = []
        for i in range(0, len(languages)):
            obj = {
                "language": languages[i],
                "language_level": levels[i]
            }
            result.append(obj)
        return result

    def online_projects(self):
        count = random.randint(2, 10)
        online_projects = []
        for i in range(1, count):
            online_projects.append(f'http://www.project-{i}.lo')
        return online_projects

    def skills(self):
        count = random.randint(2, 8)
        return self._random(self._skills, count)

    def soft_skills(self):
        return self._random(self._soft_skills, 6)

    def documents(self):
        count = random.randint(2, 3)
        return self._random(self._documents, count)

    def mobile(self):
        return '+41791234567'

    def phone(self):
        return '+41791234567'

    def distinction(self):
        return 'Distinction'

    def state(self):
        return self._random(self._state_data, 1)

    def uid(self):
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        numbers = self._random(numbers, len(numbers))
        return f'CHE-{numbers.pop(0)}{numbers.pop(0)}{numbers.pop(0)}.' \
               f'{numbers.pop(0)}{numbers.pop(0)}{numbers.pop(0)}.{numbers.pop(0)}{numbers.pop(0)}{numbers.pop(0)}'

    def description(self):
        return 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut ' \
               'labore et dolore magna aliqua. Ac tincidunt vitae semper quis lectus nulla at volutpat. Ultrices ' \
               'tincidunt arcu non sodales neque sodales ut. Velit sed ullamcorper morbi tincidunt ornare massa. Et ' \
               'tortor at risus viverra adipiscing at. Diam quis enim lobortis scelerisque fermentum.'

    def services(self):
        return 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut ' \
               'labore et dolore magna aliqua. Laoreet id donec ultrices tincidunt arcu non sodales. Ut eu sem ' \
               'integer vitae. Est velit egestas dui id ornare arcu odio.'

    def benefits(self):
        count = random.randint(2, 8)
        return self._random(self._benefits, count)

    def moods(self):
        count = random.randint(2, 7)
        return self._random(self._moods, count)

    def logo(self):
        return self._random(self._logos, 1)

    def title(self):
        return self._random(self._titles, 1)

    def workload(self):
        return self._random(self._workloads, 1)

    def number(self):
        return random.randint(1, 5)

    def requirements(self):
        count = random.randint(2, 5)
        return self._random(self._requirements, count)

    def graduation(self):
        return self._date_between('2020-01-01', '2021-12-21')
