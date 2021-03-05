import json

from django.core.management.base import BaseCommand

from db.models import Branch


class Command(BaseCommand):
    help = 'loads Branches in DB'

    def handle(self, *args, **options):
        data_set = self.read_json()
        for data in data_set:
            try:
                branch_to_update = Branch.objects.get(id=data.get('pk'))

            except Branch.DoesNotExist:
                branch_to_update = None
            if branch_to_update is not None:
                branch_to_update.name = data.get('fields').get('name')
                branch_to_update.save()

            else:
                Branch.objects.create(
                    id=data.get('pk'),
                    name=data.get('fields').get('name')
                ).save()

        self.stdout.write(self.style.SUCCESS('Filled Database'))

    def read_file(self):
        with open("db/management/data/branches.json") as file:
            data = file.read()
            file.close()
        return data

    def read_json(self):
        return json.loads(self.read_file())
