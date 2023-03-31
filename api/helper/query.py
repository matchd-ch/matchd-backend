from graphql.type import GraphQLResolveInfo
from graphql.language import NameNode


def is_me_query(info: GraphQLResolveInfo):
    query_name: NameNode = info.operation.selection_set.selections[0].name
    return query_name.value == 'me'
