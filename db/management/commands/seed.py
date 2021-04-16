import json
from django.core.management import BaseCommand

from db.seed import Seed


class Command(BaseCommand):
    help = 'Generates test data'
    data = []

    # noinspection PyUnresolvedReferences
    def handle(self, *args, **options):
        seed = Seed()
        self._load_fixtures()
        self.stdout.write('Adding test data...')
        for data in self.data:
            self.stdout.write('.', ending='')
            seed.run(data)
        self.stdout.write('', ending='\n')
        self.stdout.write(self.style.SUCCESS('Adding test data completed'))

    def _load_fixtures(self):
        with open('db/seed/data/fixtures.json') as json_file:
            self.data = json.load(json_file)
