from swh.spdx.node import Node


def assert_node(node1, node2):
    """
    Asserts if the two node objects have the same attributes.

    Args:
        node1 (Node): The first node object.
        node2 (Node): The second node object.

    Returns:
        bool: True if the node objects have the same attributes, False otherwise.
    """
    if isinstance(node1, Node) and isinstance(node2, Node):
        return (
            node1.name == node2.name
            and node1.swhid == node2.swhid
            and node1.path == node2.path
            and node1.checksums == node2.checksums
        )
    return False
