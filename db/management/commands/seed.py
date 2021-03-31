from django.core.management.base import BaseCommand

from db.management.seed import Student


class Command(BaseCommand):
    help = 'loads initial data in DB'

    seeds = [
        Student
    ]

    def handle(self, *args, **options):
        for seed in self.seeds:
            seed().run()
        self.stdout.write(self.style.SUCCESS('Seed finished'))
