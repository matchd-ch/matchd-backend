from django.utils.text import slugify

from db.models import DateMode, Student as StudentModel, JobType, Hobby, OnlineProject, UserLanguageRelation
from db.seed.base import BaseSeed


# pylint: disable=W0612
# pylint: disable=R0912
# pylint: disable=R0915
class Student(BaseSeed):

    def create_or_update(self, data, *args, **kwargs):
        if data is None:
            return None
        user = kwargs.get('user')
        student, created = StudentModel.objects.get_or_create(user=user)
        student.profile_step = data.get('profile_step')

        if student.profile_step >= 1:
            pass

        if student.profile_step >= 2:
            street = data.get('street')
            if street is None or street == '':
                street, zip_code, city = self.rand.address()
            else:
                zip_code = data.get('zip')
                city = data.get('city')
            date_of_birth = data.get('date_of_birth')
            if date_of_birth is None or date_of_birth == '':
                date_of_birth = self.rand.date_of_birth()
            mobile = data.get('mobile')
            if mobile is None or mobile == '':
                mobile = self.rand.mobile()

            student.street = street
            student.zip = zip_code
            student.city = city
            student.date_of_birth = date_of_birth
            student.mobile = mobile

        if student.profile_step >= 3:
            job_type = data.get('job_type')
            if job_type is None:
                job_type = self.rand.job_type()
            branch = data.get('branch')
            if branch is None:
                branch = self.rand.branch()

            student.job_type_id = job_type
            student.branch_id = branch

            job_type = JobType.objects.get(pk=job_type)
            job_from_date = data.get('job_from_date')
            if job_from_date is None or job_from_date == '':
                job_from_date = self.rand.job_from_date()
            job_to_date = data.get('job_to_date')
            if job_type.mode == DateMode.DATE_RANGE:
                if job_to_date is None or job_to_date == '':
                    job_to_date = self.rand.job_to_date(job_from_date)
            else:
                job_to_date = None
            student.job_from_date = job_from_date
            student.job_to_date = job_to_date

        soft_skills = []
        cultural_fits = []
        if student.profile_step >= 4:
            soft_skills = data.get('soft_skills')
            if soft_skills is None or len(soft_skills) < 6:
                soft_skills = self.rand.soft_skills()

            cultural_fits = data.get('cultural_fits')
            if cultural_fits is None or len(cultural_fits) < 6:
                cultural_fits = self.rand.cultural_fits()

        skills = []
        hobbies = []
        online_projects = []
        languages = []
        if student.profile_step >= 5:
            skills = data.get('skills')
            if skills is None:
                skills = self.rand.skills()

            distinction = data.get('distinction')
            if distinction is None or distinction == '':
                distinction = self.rand.distinction()
            student.distinction = distinction

            hobbies = data.get('hobbies')
            if hobbies is None or len(hobbies) == 0:
                hobbies = self.rand.hobbies()

            online_projects = data.get('online_projects')
            if online_projects is None or len(online_projects) == 0:
                online_projects = self.rand.online_projects()

            languages = data.get('languages')
            if languages is None or len(languages) == 0:
                languages = self.rand.languages()

        student.save()

        nickname = None
        if student.profile_step >= 6:
            nickname = data.get('nickname')
            if nickname is None or nickname == '':
                nickname = f'{user.first_name}-{user.last_name}-{student.id}'.lower()

        if student.profile_step >= 7:
            state = data.get('state')
            if state is None or state == '':
                state = self.rand.state()
            student.state = state

        student.save()

        student.soft_skills.set(soft_skills)
        student.cultural_fits.set(cultural_fits)
        student.skills.set(skills)
        for hobby in hobbies:
            Hobby.objects.get_or_create(student=student, name=hobby)
        for url in online_projects:
            OnlineProject.objects.get_or_create(student=student, url=url)
        for language in languages:
            try:
                existing = UserLanguageRelation.objects.get(student=student,
                                                            language_id=language.get('language'))
                existing.language_level_id = language.get('language_level')
                existing.save()
            except UserLanguageRelation.DoesNotExist:
                UserLanguageRelation.objects.create(
                    student=student,
                    language_id=language.get('language'),
                    language_level_id=language.get('language_level'))

        student.nickname = nickname

        # not in a form at the moment
        field_of_study = data.get('field_of_study')
        if field_of_study is None:
            field_of_study = 'Studiengang'
        student.field_of_study = field_of_study

        graduation = data.get('graduation')
        if graduation is None:
            graduation = self.rand.graduation()
        student.graduation = graduation

        school_name = data.get('school_name')
        if school_name is None:
            school_name = 'Name der Schule'
        student.school_name = school_name

        slug = data.get('slug')
        if slug is None or slug == '':
            slug = slugify(student.nickname)
        student.slug = slug

        student.save()
        return student

    def random(self, *args, **kwargs):
        index = kwargs.get('index')
        gender = self.rand.gender()
        name = self.rand.name(gender)
        first_name, last_name = name.split(' ')
        avatar = self.rand.avatar(gender)
        email = f'student-{index}@matchd.localhost'.lower()
        branch = self.rand.branch()
        street, zip_value, city = self.rand.address()
        cultural_fits = self.rand.cultural_fits()
        date_of_birth = self.rand.date_of_birth()
        distinction = self.rand.distinction()
        hobbies = self.rand.hobbies()
        job_type = self.rand.job_type()
        if job_type.mode == DateMode.DATE_FROM:
            job_from_date = self.rand.job_from_date()
            job_to_date = None
        else:
            job_from_date = self.rand.job_from_date()
            job_to_date = self.rand.job_to_date(job_from_date)
        languages = self.rand.languages()
        nickname = f'{first_name}.{last_name}'.lower()
        online_projects = self.rand.online_projects()
        skills = self.rand.skills()
        soft_skills = self.rand.soft_skills()

        attachments = [{"file": avatar, "key": "student_avatar", "type": "db.image", "user": email}]
        documents = self.rand.documents()
        for document in documents:
            attachments.append({
                "file": document,
                "key": "student_documents",
                "type": "db.file",
                "user": email
            })

        data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "student": {
                "attachments": attachments,
                "branch": branch,
                "city": city,
                "cultural_fits": cultural_fits,
                "date_of_birth": date_of_birth,
                "distinction": distinction,
                "field_of_study": "Applikationsentwicklung",
                "graduation": "2022-08-01",
                "hobbies": hobbies,
                "job_from_date": job_from_date,
                "job_to_date": job_to_date,
                "job_type": job_type,
                "languages": languages,
                "mobile": "+791234567",
                "nickname": nickname,
                "slug": slugify(nickname),
                "online_projects": online_projects,
                "profile_step": 7,
                "school_name": "FH Winterthur",
                "skills": skills,
                "soft_skills": soft_skills,
                "state": "public",
                "street": street,
                "zip": zip_value
            },
            "type": "student",
            "verified": 1
        }
        return data
