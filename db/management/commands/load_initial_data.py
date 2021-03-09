import json
import glob
from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'loads initial data in DB'

    def handle(self, *args, **options):
        files = self.get_all_json()
        for file in files:
            data_set = self.read_json(file)
            for data in data_set:
                self.get_fields(data)
                model = self.get_model(data)
                try:
                    data_to_update = model.objects.get(id=data.get('pk'))
                except model.DoesNotExist:
                    data_to_update = None
                if data_to_update is None:
                    data_to_update = model.objects.create(id=data.get('pk'))
                fields = self.get_fields(data)
                for field in fields:
                    setattr(data_to_update, field, data.get('fields').get(field))
                data_to_update.save()
            self.stdout.write(self.style.SUCCESS('Filled ' + data_set[0].get('model')))

    def read_file(self, path):
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
        return fields
