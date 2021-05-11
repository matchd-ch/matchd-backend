from django.core.management.base import BaseCommand

from db.seed import Media


class Command(BaseCommand):
    help = 'loads random media images'

    def handle(self, *args, **options):

        media = Media()
        media.run()
