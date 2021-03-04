import json

from django.core.management.base import BaseCommand, CommandError
from et_xmlfile.tests.common_imports import read_file


class Command(BaseCommand):
    help = 'loads Branches in DB'

    def handle(self, *args, **options):
        dataSet = self.read_json()

        for data in dataSet:
            Branch.objects.create(
                id=data["id"],
                name=data["name"]
            )

            self.stdout.write(self.style.SUCCESS('IT WORKS YEAHY')

    def read_file(self):
        file = open("../data/branches.json", "r")
        data = file.read()
        file.close()
        return data

    def read_json(self):
        return json.loads(self.read_file())
