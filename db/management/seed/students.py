import os

from db.helper.forms import convert_date
from db.management.seed.base import BaseSeed
from db.models import ProfileType, Student as StudentModel, AttachmentKey, UserLanguageRelation


# pylint: disable=W0221
# pylint: disable=W0511
class Student(BaseSeed):
    name = 'Student'

    def handle_item(self, user_data, index):
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        username = 'student-%s@matchd.lo' % str(index)
        user = self.create_user(username, ProfileType.STUDENT, first_name, last_name)
        self.create_student(user, user_data)
        self.add_images(user, user_data)

    def create_student(self, user, user_data):
        try:
            student = StudentModel.objects.get(user=user)
        except StudentModel.DoesNotExist:
            student = StudentModel.objects.create(user=user)

        student.mobile = user_data.get('mobile')
        student.street = user_data.get('street')
        student.zip = user_data.get('street')
        student.city = user_data.get('city')
        student.date_of_birth = convert_date(user_data.get('date_of_birth'), '%d.%m.%Y')
        student.nickname = user_data.get('nickname')
        student.school_name = user_data.get('school_name')
        student.field_of_study = user_data.get('field_of_study')
        student.graduation = convert_date(user_data.get('graduation'), '%m.%Y')
        student.job_type_id = user_data.get('job_type')
        student.job_from_date = convert_date(user_data.get('job_from_date'), '%m.%Y')
        student.job_to_date = user_data.get('job_to_date')
        student.branch_id = user_data.get('branch')
        student.skills.set(user_data.get('skills'))
        student.distinction = user_data.get('distinction')
        student.state = user_data.get('state')
        student.profile_step = user_data.get('profile_step')
        student.soft_skills.set(user_data.get('soft_skills'))
        student.cultural_fits.set(user_data.get('cultural_fits'))

        languages = user_data.get('languages')
        if languages is not None:
            for language in languages:
                UserLanguageRelation.objects.get_or_create(student=student, language_id=language.get('language'),
                                                    language_level_id=language.get('level'))

        student.save()

    def add_images(self, user, user_data):
        generated_folder = self.prepare_fixtures(False, 'student', user.username, user.id)

        avatar = user_data.get('avatar')
        profile_image_path = os.path.join(generated_folder, 'images', avatar)
        relative_image_path = os.path.join('student', str(user.id), 'images', avatar)

        image = self.create_image(user, profile_image_path, relative_image_path)
        self.create_attachment(user.student, image, AttachmentKey.STUDENT_AVATAR)
