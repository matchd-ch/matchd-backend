import pytest


@pytest.fixture
def job_posting_language_relation_valid_args(create_job_posting, create_language,
                                             create_language_level):
    return {
        'job_posting': create_job_posting,
        'language': create_language('German'),
        'language_level': create_language_level
    }
