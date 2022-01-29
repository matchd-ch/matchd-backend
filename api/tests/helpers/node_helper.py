from graphql_relay import to_global_id


def assert_node_field(node, field, value):
    assert node.get(field) == value


def assert_node_id(node, schema,id_value):
    node_id = to_global_id(schema, id_value)
    assert_node_field(node, 'id', node_id)
