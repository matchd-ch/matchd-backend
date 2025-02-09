import logging
from wagtail.search.backends import get_search_backend

from api.helper import resolve_node_ids

from db.models import ProfileType, ProfileState, ChallengeState, Challenge

logger = logging.getLogger(__name__)

# pylint: disable=W0106
# pylint: disable=R0912


def search_challenge(user, kwargs):
    text_search = kwargs.get('text_search')
    challenge_types = kwargs.get('challenge_type_ids')
    keywords = kwargs.get('keyword_ids')
    team_size = kwargs.get('team_size')
    filter_talent_challenges = kwargs.get('filter_talent_challenges', False)
    filter_company_challenges = kwargs.get('filter_company_challenges', False)
    filter_university_challenges = kwargs.get('filter_university_challenges', False)
    challenge_from_date = kwargs.get('challenge_from_date')
    date_published = kwargs.get('date_published')

    filter_conditions = []

    # do not show challenges company <-> company
    if user.is_authenticated:
        if user.type in ProfileType.valid_company_types():
            filter_conditions.append(condition("is_student_filter", True))

        # do not show challenges student <-> student
        if user.type in ProfileType.valid_student_types():
            filter_conditions.append(condition("is_company_filter", True))

    filter_conditions.append(condition('state_filter', ChallengeState.PUBLIC))

    should_conditions = [
        nested_condition('company', 'state_filter', ProfileState.PUBLIC),
        nested_condition('student', 'state_filter', ProfileState.PUBLIC),
    ]

    if challenge_types:
        filter_conditions.append(
            condition('challenge_type_id_filter', resolve_node_ids(challenge_types), "terms"))

    if keywords:
        filter_conditions.append(
            condition('challenge_keywords_filter', resolve_node_ids(keywords), "terms"))

    if team_size is not None:
        filter_conditions.append(condition('team_size_filter', team_size))

    if challenge_from_date is not None:
        filter_conditions.append(
            {'range': {
                'challenge_from_date_filter': {
                    'gte': challenge_from_date
                }
            }})

    if date_published is not None:
        filter_conditions.append({'range': {'date_published_filter': {'gte': date_published}}})

    posting_entity_query = []

    if filter_talent_challenges:
        posting_entity_query.append(condition("is_student_filter", True))

    if filter_company_challenges:
        posting_entity_query.append(nested_condition('company', 'type_filter',
                                                     ProfileType.COMPANY)),

    if filter_university_challenges:
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
        "index": [get_search_backend().get_index_for_model(Challenge).name],
        "body": {
            "query": {
                "bool": {
                    "filter": filter_conditions,
                    "should": should_conditions
                },
            },
            "size": 10000
        },
        "_source": False
    }

    try:
        results = get_search_backend().es.search(**params)
    except Exception as exception:
        logger.error("Failed to search using elasticsearch: %s", str(exception))

        return None

    return results


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
