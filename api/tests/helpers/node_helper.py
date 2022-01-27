import base64


def b64encode_string(string):
    return base64.b64encode(f'{string}'.encode('utf-8')).decode('utf-8')


def assert_node_field(node, field, value):
    assert node.get(field) == value


def assert_node_id(node, node_id):
    b64_encoded_id = b64encode_string(node_id)
    assert_node_field(node, 'id', b64_encoded_id)
