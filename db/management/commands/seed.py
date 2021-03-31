from django.core.management.base import BaseCommand

from db.management.seed import Student, Company


class Command(BaseCommand):
    help = 'Generates test data'

    # noinspection PyUnresolvedReferences
    def handle(self, *args, **options):

        seeds = [
            Student(stdout=self.stdout, file='students.json'),
            Company(stdout=self.stdout, file='companies.json')
        ]

        for seed in seeds:
            seed.run()
        self.stdout.write(self.style.SUCCESS('Seed finished'))
