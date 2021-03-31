import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand

from db.management.seed import Student, Company


class Command(BaseCommand):
    help = 'Generates test data'

    # noinspection PyUnresolvedReferences
    def handle(self, *args, **options):

        fixtures_dir = os.path.join(settings.BASE_DIR, '..', 'media-fixtures')

        if not os.path.exists(fixtures_dir):
            print('Missing media_fixtures: ', fixtures_dir)
            print('Ensure media_fixtures are up to date. Run ./init.sh')
            raise Exception('Missing media fixtures')

        for file_or_directory in os.scandir(fixtures_dir):
            if os.path.isdir(file_or_directory):
                if file_or_directory.name[0] != '.':
                    dir_to_copy = os.path.join(fixtures_dir, file_or_directory.name)
                    destination = os.path.join(settings.MEDIA_ROOT, file_or_directory.name)
                    if os.path.exists(destination):
                        shutil.rmtree(destination)
                    shutil.copytree(dir_to_copy, destination)

        seeds = [
            Student(stdout=self.stdout, file='students.json'),
            Company(stdout=self.stdout, file='companies.json')
        ]

        for seed in seeds:
            seed.run()
        self.stdout.write(self.style.SUCCESS('Seed finished'))
