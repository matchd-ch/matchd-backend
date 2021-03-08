import json
import glob
from django.core.management.base import BaseCommand
from db.models import Branch
from django.apps import apps




class Command(BaseCommand):
    help = 'loads Branches in DB'

    def handle(self, *args, **options):
        files = self.get_all_json()
        for file in files:

            data_set = self.read_json(file)

            for data in data_set:
                self.get_fields(data)
                model = self.get_model(data)
                try:
                    branch_to_update = model.objects.get(id=data.get('pk'))

                except model.DoesNotExist:
                    branch_to_update = None
                if branch_to_update is not None:
                    branch_to_update.name = data.get('fields').get('name')
                    branch_to_update.save()

                else:
                    model.objects.create(
                        id=data.get('pk'),
                        name=data.get('fields').get('name')
                    ).save()

            self.stdout.write(self.style.SUCCESS('Filled Database'))

    def read_file(self, path):
        # db/management/data/branches.json
        with open(path) as file:
            data = file.read()
            file.close()
        return data

    def read_json(self, path):
        return json.loads(self.read_file(path))

    def get_all_json(self):
        base_path = 'db/management/data'
        return glob.glob(base_path + "/*.json")

    def get_model(self, data):
        data_model = data.get('model').split(".")
        return apps.get_model(app_label='db', model_name=data_model[1])

    def get_fields(self, data):
        fields = data.get('fields').keys()
        print(fields)
        return fields


