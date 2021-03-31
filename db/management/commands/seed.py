from django.core.management.base import BaseCommand

from db.management.seed import Student, Company


class Command(BaseCommand):
    help = 'Generates test data'

    # noinspection PyUnresolvedReferences
    def handle(self, *args, **options):
        self.stdout.write('Adding test data...')
        seeds = [
            Student(stdout=self.stdout, style=self.style, file='students.json'),
            Company(stdout=self.stdout, style=self.style, file='companies.json')
        ]

        for seed in seeds:
            seed.run()
        self.stdout.write(self.style.SUCCESS('Adding test data completed'))
