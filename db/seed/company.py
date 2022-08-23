from db.seed.base import BaseSeed
from db.models import Company as CompanyModel, ProfileType


# pylint: disable=R0912
# pylint: disable=R0915
# pylint: disable=W0612
class Company(BaseSeed):

    def create_or_update(self, data, *args, **kwargs):
        if data is None:
            return None
        user = kwargs.get('user')
        company, created = CompanyModel.objects.get_or_create(slug=data.get('slug'))
        user.company = company
        user.save()

        if len(data.keys()) == 1:
            return company

        company.profile_step = data.get('profile_step')
        company.state = data.get('state')
        company.type = data.get('type')
        if company.type == ProfileType.COMPANY:
            self._create_or_update_company(company, user, data)
        if company.type == ProfileType.UNIVERSITY:
            self._create_or_update_university(company, user, data)
        return company

    def _create_or_update_university(self, company, user, data):

        zip_code = data.get('zip')
        if zip_code is None or zip_code == '':
            street, zip_code, city = self.rand.address()
        else:
            city = data.get('city')
            street = data.get('street')

        if company.profile_step >= 1:
            name = data.get('name')
            if name is None or name == '':
                name = f'{user.last_name} AG'

            role = data.get('role')
            if role is None or role == '':
                role = 'Rector'

            company.uid = ''
            company.name = name
            company.zip = zip_code
            company.city = city
            company.street = ''

            user.employee.role = role

        if company.profile_step >= 2:

            phone = data.get('phone')
            if phone is None or phone == '':
                phone = self.rand.phone()

            company.phone = phone

            company.street = street

            website = data.get('website')
            if website is None or website == '':
                website = f'https://www.{user.last_name}-university.lo'.lower()

            top_level_website = data.get('top_level_organisation_website')
            if top_level_website is None or top_level_website == '':
                top_level_website = f'https://www.{user.last_name}-university.lo'.lower()

            top_level_description = data.get('top_level_organisation_description')
            if top_level_description is None or top_level_description == '':
                top_level_description = self.rand.description()

            company.website = website
            company.top_level_organisation_website = top_level_website
            company.top_level_organisation_description = top_level_description

        branches = []
        benefits = []
        if company.profile_step >= 3:
            description = data.get('description')
            if description is None or description == '':
                description = self.rand.description()

            branches = data.get('branches')
            if branches is None or len(branches) == 0:
                branches = self.rand.branches()

            benefits = data.get('benefits')
            if benefits is None or len(benefits) == 0:
                benefits = self.rand.benefits()

            company.description = description

        soft_skills = []
        cultural_fits = []
        if company.profile_step >= 4:
            services = data.get('services')
            if services is None or services == '':
                services = self.rand.description()

            company.services = services

            link_education = data.get('link_education')
            if link_education is None or link_education == '':
                link_education = 'https://www.education.lo'

            link_challenges = data.get('link_challenges')
            if link_challenges is None or link_challenges == '':
                link_challenges = 'https://www.challenges.lo'

            link_thesis = data.get('link_thesis')
            if link_thesis is None or link_thesis == '':
                link_thesis = 'https://www.thesis.lo'

            soft_skills = data.get('soft_skills')
            if soft_skills is None or len(soft_skills) == 0:
                soft_skills = self.rand.soft_skills()

            cultural_fits = data.get('cultural_fits')
            if cultural_fits is None or len(cultural_fits) == 0:
                cultural_fits = self.rand.cultural_fits()

            company.link_education = link_education
            company.link_challenges = link_challenges
            company.link_thesis = link_thesis

        company.save()
        company.branches.set(branches)
        company.benefits.set(benefits)
        company.soft_skills.set(soft_skills)
        company.cultural_fits.set(cultural_fits)

    def _create_or_update_company(self, company, user, data):
        uid = data.get('uid')
        if uid is None or uid == '':
            uid = self.rand.uid()
        company.uid = uid

        zip_code = data.get('zip')
        if zip_code is None or zip_code == '':
            street, zip_code, city = self.rand.address()
        else:
            city = data.get('city')
            street = data.get('street')

        if company.profile_step >= 1:
            name = data.get('name')
            if name is None or name == '':
                name = f'{user.last_name} AG'

            role = data.get('role')
            if role is None or role == '':
                role = 'Recruiter'
            company.name = name
            company.zip = zip_code
            company.city = city
            company.street = ''

            user.employee.role = role

        if company.profile_step >= 2:
            company.street = street

            phone = data.get('phone')
            if phone is None or phone == '':
                phone = self.rand.phone()

            company.phone = phone

        if company.profile_step >= 3:
            website = data.get('website')
            if website is None or website == '':
                website = f'https://www.{user.last_name}-ag.lo'.lower()

            description = data.get('description')
            if description is None or description == '':
                description = self.rand.description()

            services = data.get('services')
            if services is None or services == '':
                services = self.rand.services()

            member_it_st_gallen = data.get('member_it_st_gallen')
            if member_it_st_gallen is None or member_it_st_gallen == '':
                member_it_st_gallen = True

            company.website = website
            company.description = description
            company.services = services
            company.member_it_st_gallen = member_it_st_gallen

        branches = []
        benefits = []
        if company.profile_step >= 4:
            branches = data.get('branches')
            if branches is None or len(branches) == 0:
                branches = self.rand.branches()

            benefits = data.get('benefits')
            if benefits is None or len(benefits) == 0:
                benefits = self.rand.benefits()

        soft_skills = []
        cultural_fits = []
        if company.profile_step >= 4:
            soft_skills = data.get('soft_skills')
            if soft_skills is None or len(soft_skills) == 0:
                soft_skills = self.rand.soft_skills()

            cultural_fits = data.get('cultural_fits')
            if cultural_fits is None or len(cultural_fits) == 0:
                cultural_fits = self.rand.cultural_fits()

        company.save()
        company.branches.set(branches)
        company.benefits.set(benefits)
        company.soft_skills.set(soft_skills)
        company.cultural_fits.set(cultural_fits)

    def random(self, *args, **kwargs):

        company_type = kwargs.get('company_type')
        index = kwargs.get('index')

        email = f"dummy-company-{index}-1@matchd.localhost"
        role = 'Recruiter'
        slug = f'dummy-company-{index}'
        if company_type == ProfileType.UNIVERSITY:
            email = f"dummy-university-{index}-1@matchd.localhost"
            role = 'Rector'
            slug = f'dummy-university-{index}'

        attachments = []
        avatar = self.rand.logo()
        moods = self.rand.moods()
        attachments.append({
            "file": f"avatars/{avatar}",
            "key": "company_avatar",
            "type": "db.image",
            "user": email
        })
        for mood in moods:
            attachments.append({
                "file": f"moods/{mood}",
                "key": "company_documents",
                "type": "db.image",
                "user": email
            })

        street, zip_code, city = self.rand.address()
        gender = self.rand.gender()
        name = self.rand.name(gender)
        first_name, last_name = name.split(' ')
        data = {
            "company": {
                "attachments": attachments,
                "benefits": [],
                "branches": self.rand.branches(),
                "city": city,
                "cultural_fits": [],
                "description": self.rand.description(),
                "job_postings": [],
                "link_education": "",
                "link_challenges": "",
                "link_thesis": "",
                "member_it_st_gallen": False,
                "name": "",
                "phone": self.rand.phone(),
                "profile_step": 5,
                "slug": slug,
                "uid": "",
                "website": "",
                "services": "",
                "soft_skills": [],
                "state": "public",
                "street": street,
                "top_level_organisation_description": "",
                "top_level_organisation_website": "",
                "type": company_type,
                "zip": zip_code
            },
            "email": email,
            "employee": {
                "role": role
            },
            "first_name": first_name,
            "last_name": last_name,
            "type": company_type,
            "verified": True
        }

        if company_type == ProfileType.COMPANY:
            data['company']['uid'] = self.rand.uid()
            data['company']['website'] = f"https://www.{last_name}-ag.lo".lower()
            data['company']['services'] = self.rand.services()
            data['company']['member_it_st_gallen'] = False
            data['company']['soft_skills'] = self.rand.soft_skills()
            data['company']['cultural_fits'] = self.rand.cultural_fits()
            data['company']['name'] = f"{last_name} AG"
            data['company']['benefits'] = self.rand.benefits()

        if company_type == ProfileType.UNIVERSITY:
            data['company']['name'] = f"{last_name} University"
            data['company']['top_level_organisation_description'] = self.rand.description()
            data['company']['top_level_organisation_website'] = "https://www.toplevel.lo"
            data['company']['link_education'] = "https://www.edu.lo"
            data['company']['link_challenges'] = "https://www.challenges.lo"
            data['company']['link_thesis'] = "https://www.thesis.lo"
            data['company']['soft_skills'] = self.rand.soft_skills()
            data['company']['cultural_fits'] = self.rand.cultural_fits()
            data['company']['benefits'] = self.rand.benefits()

        return data
