from swh.spdx.node import Node


def generate_spdx() -> None:
    """
    Generate spdx document
    """
    pass


def traverse_merkle_dag(
    node: Node, parent_path: str = "", first_iteration: bool = False
) -> None:
    """
    Recursively traverses the merkle DAG and sets the path for each node.

    Args:
        node (Node): The current node to process.
        parent_path (str): The path of the parent node.

    """
    # Set the path for the current node
    if not first_iteration:
        node.set_path(parent_path)

    if node.is_directory():
        # Recursively process children nodes
        for child_name, child_properties in node.get_children().items():
            child_swhid = child_properties[0]

            child = Node(name=child_name, swhid=child_swhid)

            child.set_checksums(child_properties)

            traverse_merkle_dag(child, node.path)
    else:
        generate_spdx()


"""
root_node = Node(name="root", swhid="swh:1:dir:root")  # Replace with your root node
traverse_merkle_dag(root_node)
"""
