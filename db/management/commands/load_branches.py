import json

from django.core.management.base import BaseCommand

from db.models import Branch


class Command(BaseCommand):
    help = 'loads Branches in DB'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear Database before filling',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.clear_branches()
            self.stdout.write(self.style.SUCCESS('Cleared Branches'))
            return

        data_set = self.read_json()

        for data in data_set:
            Branch.objects.create(
                id=data["id"],
                name=data["name"]
            ).save()
        self.stdout.write(self.style.SUCCESS('Filled Database'))

    def read_file(self):
        file = open("db/management/data/branches.json", "r")
        data = file.read()
        file.close()
        return data

    def read_json(self):
        return json.loads(self.read_file())

    def clear_branches(self):
        Branch.objects.all().delete()
