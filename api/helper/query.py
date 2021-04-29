from graphql import ResolveInfo
from graphql.language.ast import Name


def is_me_query(info: ResolveInfo):
    query_name: Name = info.operation.selection_set.selections[0].name
    return query_name.value == 'me'


def is_faq_categories_query(info: ResolveInfo):
    query_name: Name = info.operation.selection_set.selections[0].name
    return query_name.value == 'faqCategories'
