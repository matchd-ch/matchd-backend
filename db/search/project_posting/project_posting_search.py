from wagtail.search.backends import get_search_backend

from api.helper import resolve_node_ids

from db.models import ProfileType, ProfileState, ProjectPostingState, ProjectPosting

# pylint: disable=W0106


def search_project_posting(user, kwargs):
    text_search = kwargs.get('text_search')
    project_types = kwargs.get('project_type_ids')
    keywords = kwargs.get('keyword_ids')
    team_size = kwargs.get('team_size')
    filter_talent_projects = kwargs.get('filter_talent_projects', False)
    filter_company_projects = kwargs.get('filter_company_projects', False)
    filter_university_projects = kwargs.get('filter_university_projects', False)
    project_from_date = kwargs.get('project_from_date')
    date_published = kwargs.get('date_published')

    filter_conditions = []

    # do not show project postings company <-> company
    if user.is_authenticated:
        if user.type in ProfileType.valid_company_types():
            filter_conditions.append(condition("is_student_filter", "true"))

        # do not show project postings student <-> student
        if user.type in ProfileType.valid_student_types():
            filter_conditions.append(condition("is_company_filter", "true"))

    filter_conditions.append(condition('state_filter', ProjectPostingState.PUBLIC))

    should_conditions = [
        nested_condition('company', 'state_filter', ProfileState.PUBLIC),
        nested_condition('student', 'state_filter', ProfileState.PUBLIC),
    ]

    if project_types:
        filter_conditions.append(
            condition('project_type_id_filter', resolve_node_ids(project_types), "terms"))

    if keywords:
        filter_conditions.append(
            condition('project_keywords_filter', resolve_node_ids(keywords), "terms"))

    if team_size is not None:
        filter_conditions.append(condition('team_size_filter', team_size))

    if project_from_date is not None:
        filter_conditions.append(
            {'range': {
                'project_from_date_filter': {
                    'gte': project_from_date
                }
            }})

    if date_published is not None:
        filter_conditions.append({'range': {'date_published_filter': {'gte': date_published}}})

    posting_entity_query = []

    if filter_talent_projects:
        posting_entity_query.append(condition("is_student_filter", "true"))

    if filter_company_projects:
        posting_entity_query.append(nested_condition('company', 'type_filter',
                                                     ProfileType.COMPANY)),

    if filter_university_projects:
        posting_entity_query.append(
            nested_condition('company', 'type_filter', ProfileType.UNIVERSITY)),

    filter_conditions.append({"bool": {"should": posting_entity_query}})

    if text_search is not None:
        filter_conditions.append(
            {"multi_match": {
                "query": text_search,
                "fields": ["title", "description"]
            }})

    params = {
        "index": [get_search_backend().get_index_for_model(ProjectPosting).name],
        "body": {
            "query": {
                "bool": {
                    "filter": filter_conditions,
                    "should": should_conditions
                },
            },
            "size": 10000
        },
        "_source": False,
        "stored_fields": "pk",
    }

    return get_search_backend().es.search(**params)


def condition(prop, value, occurence_type="term"):
    return {occurence_type: {prop: value}}


def nested_condition(path, prop, value):
    return {
        "nested": {
            "path": path,
            "query": {
                "term": {
                    f"{path}.{prop}": value
                }
            }
        },
    }
