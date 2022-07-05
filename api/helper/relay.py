from graphql_relay.node.node import from_global_id

# pylint: disable=W0102


def input_to_dictionary(data: dict, id_fields: list[str] = ['id']) -> dict:
    dictionary = {}
    for field in data:
        # Convert GraphQL global id to database id
        if field in id_fields:
            data[field] = resolve_node_id(data[field])
        else:
            data[field] = resolve_node_ids(data[field], id_fields)
        dictionary[field] = data[field]
    return dictionary


def resolve_node_ids(data: any, id_fields: list[str] = ['id']) -> any:
    result = data

    if isinstance(data, list):
        result = list(map(lambda element: resolve_node_ids(element, id_fields), data))

    if isinstance(data, dict):
        result = input_to_dictionary(data, id_fields)

    return result


def resolve_node_id(node_id: str) -> str:
    if not node_id:
        return None

    return from_global_id(node_id)[1]


def extract_ids(elements: list, id_field: str) -> list[str]:
    return list(map(lambda element: element.get(id_field), elements))
