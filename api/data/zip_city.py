import json

from django.conf import settings


class ZipCity:

    def __init__(self):
        with open(settings.ZIP_CITY_DATA_SOURCE, encoding='utf-8') as json_file:
            self.data = json.load(json_file)


zip_city_datasource = ZipCity()
