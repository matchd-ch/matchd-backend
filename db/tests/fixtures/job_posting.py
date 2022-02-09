from datetime import date

import pytest

from db.models.job_posting import JobPosting


@pytest.fixture
def job_posting_valid_args(create_job_type, create_company, create_employee):
    return {
        'title': 'A nice job',
        'slug': 'Nice job',
        'description': 'Apply for this nice job.',
        'job_type': create_job_type,
        'workload': 100,
        'company': create_company,
        'job_from_date': date(2022, 2, 10),
        'job_to_date': date(2024, 2, 10),
        'url': 'www.joburl.ch',
        'employee': create_employee,
        'date_published': date(2024, 2, 15),
    }


@pytest.fixture
def create_job_posting(create_company, create_job_type):
    return JobPosting.objects.create(title='Test',
                                     company=create_company,
                                     job_type=create_job_type,
                                     job_from_date=date(2022, 2, 10))
