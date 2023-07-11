from swh.spdx.node import Node


def traverse_root(
    node: Node, first_iteration: bool = False, node_collection: dict = {}
) -> dict:
    """
    Recursively traverses the root directory and collects each node found.

    Args:
        node (Node): The current node to process.
        first_iteration (bool): represents if the iteration is first or not
        node_collection (dict): collection of nodes found

    Returns:
        node_collection (dict): Collection of nodes found in the root directory,
        with keys as root-directory or sub-directories and value as a list of child nodes
    """
    # Set the path for the root directory node

    if first_iteration:
        node.path = node.name

    if node.is_directory:
        # Initializing node_collection with key as a root-directory or sub-directory
        # and value as empty list which will then contain all children nodes
        node_collection[node] = []
        for (
            child_name,
            child_properties,
        ) in node.get_children().items():
            child_swhid = child_properties[0]
            child = Node(name=child_name, swhid=child_swhid)
            child.set_checksums(child_properties)
            child.set_path(child_properties)
            # Appending each child node found to the 'value' list of 'key' directory
            node_collection[node].append(child)
            traverse_root(node=child, node_collection=node_collection)
    return node_collection
