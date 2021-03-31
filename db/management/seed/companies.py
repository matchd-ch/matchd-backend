import os

from db.management.seed.base import BaseSeed
from db.models import Company as CompanyModel, ProfileState, Employee as EmployeeModel, AttachmentKey


# pylint: disable=W0221
# pylint: disable=W0511
class Company(BaseSeed):

    def handle_item(self, company_data, index):
        company_type = company_data.get('type')
        slug = 'company-%s' % str(index)
        employees = company_data.get('employees')

        try:
            company = CompanyModel.objects.get(slug=slug)
        except CompanyModel.DoesNotExist:
            company = CompanyModel.objects.create(
                type=company_type,
                state=ProfileState.PUBLIC,
                slug=slug
            )

        company.profile_step = company_data.get('profile_step')
        company.name = company_data.get('name')
        company.zip = company_data.get('zip')
        company.city = company_data.get('city')
        company.street = company_data.get('street')
        company.phone = company_data.get('phone')
        company.website = company_data.get('website')
        company.branch = company_data.get('branch')
        company.description = company_data.get('description')
        company.soft_skills.set(company_data.get('soft_skills'))

        # company only fields
        company.uid = company_data.get('uid', '')
        company.services = company_data.get('services', '')
        company.member_it_st_gallen = company_data.get('member_it_st_gallen', 0)
        # TODO add job positions
        company.cultural_fits.set(company_data.get('cultural_fits', []))

        # university only fields
        company.top_level_organisation_website = company_data.get('top_level_organisation_website', '')
        company.top_level_organisation_description = company_data.get('top_level_organisation_description', '')
        company.link_education = company_data.get('link_education', None)
        company.link_projects = company_data.get('link_projects', None)
        company.link_thesis = company_data.get('link_thesis', None)

        company.save()

        employee_index = 1
        for employee_data in employees:
            first_name = employee_data.get('first_name')
            last_name = employee_data.get('last_name')
            username = 'company-%s-%s@matchd.lo' % (str(index), str(employee_index))

            user = self.create_user(username, company_type, first_name, last_name, company)
            self.create_employee(user, employee_data)
            employee_index += 1

        self.add_images(company)
        # TODO create job postings

    def create_employee(self, user, employee_data):
        try:
            employee = EmployeeModel.objects.get(user=user)
        except EmployeeModel.DoesNotExist:
            employee = EmployeeModel.objects.create(user=user)

        employee.role = employee_data.get('role')
        employee.save()

    def add_images(self, company):
        generated_folder = self.prepare_fixtures(True, 'company', 'company', company.id)

        company_user = company.users.all()[0]

        # images
        for i in range(1, 5):
            image_name = 'image_%s.jpg' % str(i)
            image_path = os.path.join(generated_folder, 'images', image_name)
            relative_image_path = os.path.join('company', str(company.id), 'images', image_name)

            image = self.create_image(company_user, image_path, relative_image_path)
            self.create_attachment(company, image, AttachmentKey.COMPANY_DOCUMENTS)

        profile_image_path = os.path.join(generated_folder, 'images', 'logo.png')
        relative_image_path = os.path.join('company', str(company.id), 'images', 'logo.png')

        image = self.create_image(company_user, profile_image_path, relative_image_path)
        self.create_attachment(company, image, AttachmentKey.COMPANY_AVATAR)
