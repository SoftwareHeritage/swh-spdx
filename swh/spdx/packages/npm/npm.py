from spdx_tools.spdx.model import Document
from spdx_tools.spdx.writer.write_anything import write_file

from swh.model.swhids import CoreSWHID
from swh.spdx.node import Node
from swh.spdx.packages.base import get_metadata_node, set_files
from swh.spdx.packages.creation_info import set_creation_info
from swh.spdx.packages.npm.utils import (
    get_dependency_packages,
    set_dependency_packages,
    set_top_level_package,
)
from swh.spdx.traverse import traverse_root


def generate_spdx(root_swhid: CoreSWHID, path: str):
    """
    Generates the spdx document and writes it in the current directory

    Args:
        root_swhid (CoreSWHID): swhid of root directory
    """
    # Assuming the root directory as ./ specified by the SPDX specification
    root_node = Node(name=".", swhid=root_swhid)
    node_collection = traverse_root(node=root_node, first_iteration=True)
    top_level_package_node = node_collection[root_node][0]
    # Setting up CreationInfo
    creation_info = set_creation_info(top_level_package_node.name)
    spdx_document = Document(creation_info)
    metadata_node = get_metadata_node(node_collection)
    # Implementing Top-level package
    (
        top_level_package,
        top_level_package_relationships,
        top_level_package_spdx_id,
        metadata_dict,
    ) = set_top_level_package(
        package_node=top_level_package_node,
        node_collection=node_collection,
        metadata_node=metadata_node,
    )

    # Implementing Dependency packages
    dependency_packages_list = get_dependency_packages(metadata_dict)
    dependency_packages, dependency_package_relationships = set_dependency_packages(
        dependency_packages=dependency_packages_list,
        top_level_package_spdx_id=top_level_package_spdx_id,
    )

    # Implementing Top-level package files
    files, file_relationships = set_files(node_collection, top_level_package_spdx_id)

    spdx_packages = top_level_package + dependency_packages
    spdx_package_relationships = (
        top_level_package_relationships
        + dependency_package_relationships
        + file_relationships
    )

    spdx_document.packages = spdx_packages
    spdx_document.relationships = spdx_package_relationships
    spdx_document.files = files

    # Writes the spdx document in the specified apth
    path_to_write = f"{path}/{top_level_package_node.name}.spdx.json"
    write_file(spdx_document, path_to_write)
