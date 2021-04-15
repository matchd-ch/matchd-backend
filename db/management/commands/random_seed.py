from django.core.management import BaseCommand
from ...seed import Seed
from db.models import ProfileType


class Command(BaseCommand):
    help = 'Generates random students'

    seed = Seed()

    def add_arguments(self, parser):
        parser.add_argument('num_students', type=int, help='Indicates the number of students to be created', default=0)
        parser.add_argument('num_companies', type=int, help='Indicates the number of companies to be created',
                            default=0)
        parser.add_argument('num_universities', type=int, help='Indicates the number of universities to be created',
                            default=0)

    # noinspection PyUnresolvedReferences
    def handle(self, *args, **options):
        number_of_students = options.get('num_students')
        number_of_companies = options.get('num_companies')
        number_of_universities = options.get('num_universities')

        self.stdout.write(f'Adding {number_of_students} random student(s)...')
        for i in range(0, number_of_students):
            self.stdout.write('.', ending='')
            random_data = self.seed.random_student(i)
            self.seed.run(random_data)
        self.stdout.write('', ending='\n')

        self.stdout.write(f'Adding {number_of_companies} random company(ies)...')
        for i in range(0, number_of_companies):
            self.stdout.write('.', ending='')
            random_data = self.seed.random_company(i, ProfileType.COMPANY)
            self.seed.run(random_data)
        self.stdout.write('', ending='\n')

        self.stdout.write(f'Adding {number_of_companies} random company(ies)...')
        for i in range(0, number_of_universities):
            self.stdout.write('.', ending='')
            random_data = self.seed.random_company(i, ProfileType.UNIVERSITY)
            self.seed.run(random_data)
        self.stdout.write('', ending='\n')
        self.stdout.write(self.style.SUCCESS('Adding random data completed'))
