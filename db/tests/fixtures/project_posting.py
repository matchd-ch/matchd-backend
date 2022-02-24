from datetime import date

import pytest


@pytest.fixture
def project_posting_valid_args(create_employee, create_student, create_company, create_project_type,
                               create_topic):
    return {
        'title': 'Interesting project',
        'slug': 'interesting-project',
        'project_type': create_project_type,
        'topic': create_topic,
        'description': 'An interesting project.',
        'additional_information': 'Everyone should apply.',
        'website': 'www.amazingproject.ch',
        'project_from_date': date(2022, 3, 25),
        'employee': create_employee,
        'student': create_student,
        'company': create_company,
        'form_step': 2,
        'state': 'Open',
        'date_published': date(2022, 2, 27)
    }