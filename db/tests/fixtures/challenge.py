from datetime import date

import pytest


@pytest.fixture
def challenge_valid_args(create_employee, create_student, create_company, create_challenge_type):
    return {
        'title': 'Interesting challenge',
        'slug': 'interesting-challenge',
        'challenge_type': create_challenge_type,
        'description': 'An interesting challenge.',
        'team_size': 5,
        'compensation': 'To be discussed.',
        'website': 'www.amazingchallenge.ch',
        'challenge_from_date': date(2022, 3, 25),
        'employee': create_employee,
        'student': create_student,
        'company': create_company,
        'form_step': 2,
        'state': 'Open',
        'date_published': date(2022, 2, 27)
    }
