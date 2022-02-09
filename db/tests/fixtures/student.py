from datetime import date

import pytest

from db.models.profile_state import ProfileState
from db.models.student import Student


@pytest.fixture
def student_valid_args(create_user, create_branch, create_job_type):
    return {
        'user': create_user,
        'mobile': '0279929444',
        'street': 'Teststrasse 1',
        'zip': '9000',
        'city': 'St. Gallen',
        'date_of_birth': date(2001, 3, 17),
        'nickname': 'Hey',
        'school_name': 'Someschool',
        'field_of_study': 'Computer Science',
        'graduation': date(2021, 1, 10),
        'branch': create_branch,
        'job_type': create_job_type,
        'job_from_date': date(2021, 1, 11),
        'job_to_date': date(2022, 1, 20),
        'distinction': 'Experienced',
        'state': ProfileState.ANONYMOUS,
        'profile_step': 1,
        'slug': 'jd'
    }


@pytest.fixture
def create_student(create_user):
    return Student.objects.create(user=create_user,
                                  mobile='0279929444',
                                  city='St. Gallen',
                                  slug='jd')
