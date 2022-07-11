import datetime
import pytest

from django.contrib.auth.models import AnonymousUser

from graphql_relay import to_global_id

from db.models import ProfileState


@pytest.mark.django_db
def test_project_postings_filter_project_type(query_project_postings, user_student_full_profile,
                                              company_project_posting_objects,
                                              student_project_posting_objects):
    user_student_full_profile.student.state = ProfileState.PUBLIC
    user_student_full_profile.student.save()

    data, errors = query_project_postings(
        AnonymousUser(), {
            'projectTypeId':
            f"\"{to_global_id('ProjectType', company_project_posting_objects[0].project_type_id)}\""
        })
    assert errors is None
    assert data is not None

    edges = data.get('projectPostings').get('edges')
    assert edges is not None
    assert len(edges) == 4


@pytest.mark.django_db
def test_project_postings_filter_keywords(query_project_postings, user_student_full_profile,
                                          keyword_objects, company_project_posting_objects,
                                          student_project_posting_objects):
    user_student_full_profile.student.state = ProfileState.PUBLIC
    user_student_full_profile.student.save()

    company_project_posting_objects[0].keywords.set([obj.id for obj in keyword_objects])
    student_project_posting_objects[1].keywords.set([keyword_objects[0].id])

    data, errors = query_project_postings(
        AnonymousUser(),
        {'keywordIds': [f"\"{to_global_id('Keywords', obj.id)}\"" for obj in keyword_objects]})
    assert errors is None
    assert data is not None

    edges = data.get('projectPostings').get('edges')
    assert edges is not None
    assert len(edges) == 2


@pytest.mark.django_db
def test_project_postings_filter_team_size(query_project_postings, user_student_full_profile,
                                           company_project_posting_objects,
                                           student_project_posting_objects):
    user_student_full_profile.student.state = ProfileState.PUBLIC
    user_student_full_profile.student.save()

    data, errors = query_project_postings(AnonymousUser(), {'teamSize': 10})
    assert errors is None
    assert data is not None

    edges = data.get('projectPostings').get('edges')
    assert edges is not None
    assert len(edges) == 1


@pytest.mark.django_db
def test_project_postings_filter_project_from_date(query_project_postings,
                                                   user_student_full_profile,
                                                   company_project_posting_objects,
                                                   student_project_posting_objects):
    user_student_full_profile.student.state = ProfileState.PUBLIC
    user_student_full_profile.student.save()

    company_project_posting_objects[0].project_from_date = datetime.datetime(2020, 3, 18).date()
    company_project_posting_objects[0].save()

    student_project_posting_objects[1].project_from_date = datetime.datetime(2020, 3, 18).date()
    student_project_posting_objects[1].save()

    data, errors = query_project_postings(
        AnonymousUser(), {'projectFromDate': f"\"{datetime.datetime(2020, 2, 20).date()}\""})
    assert errors is None
    assert data is not None

    edges = data.get('projectPostings').get('edges')
    assert edges is not None
    assert len(edges) == 2


@pytest.mark.django_db
def test_project_postings_filter_company(query_project_postings, company_object_complete,
                                         company_project_posting_objects):
    data, errors = query_project_postings(
        AnonymousUser(),
        {'companyId': f"\"{to_global_id('Company', company_object_complete.id)}\""})
    assert errors is None
    assert data is not None

    edges = data.get('projectPostings').get('edges')
    assert edges is not None
    assert len(edges) == len(company_project_posting_objects) - 1


@pytest.mark.django_db
def test_project_postings_filter_date_published(query_project_postings, user_student_full_profile,
                                                company_project_posting_objects,
                                                student_project_posting_objects):
    user_student_full_profile.student.state = ProfileState.PUBLIC
    user_student_full_profile.student.save()

    student_project_posting_objects[1].date_published = datetime.datetime(2020, 3, 18).date()
    student_project_posting_objects[1].save()

    data, errors = query_project_postings(
        AnonymousUser(), {'datePublished': f"\"{datetime.datetime(2020, 2, 20).date()}\""})
    assert errors is None
    assert data is not None

    edges = data.get('projectPostings').get('edges')
    assert edges is not None
    assert len(edges) == 1
