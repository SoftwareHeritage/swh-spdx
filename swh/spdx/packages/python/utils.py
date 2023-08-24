from typing import Tuple

from spdx_tools.spdx.model import Package, Relationship, RelationshipType

from swh.spdx.content import get_content_from_hashes
from swh.spdx.node import Node
from swh.spdx.packages.python.spdx_fields import (
    DependencyPackagePython,
    TopLevelPackagePython,
)


def get_dependency_packages(node_collection: dict, root_node: Node):
    """
    Detects potential dependencies of a Python project based on various sources.

    Args:
        node_collection (dict): Collection of nodes found in the root directory,
            with keys as root-directory or sub-directories and value as a list of child nodes
            and also contains an extra key "METADATA_NODE" with value as the metadata file node
            which the tool currently supports
        root_node (Node): root node of the directory structure representing root directory node

    Returns:
        dependency_packages (list): A list of detected potential dependencies.

    Note:
        This function attempts to identify potential dependencies based on common patterns
        but does not cover all possible sources of dependencies. It currently supports
        detection from common dependency management files like 'requirements.txt'.

        The dependency detection can be complex due to variations in project
        structures and practices. The use of 'requirements.txt' files is recommended by PEP 508,
        but it's not mandatory. Therefore, this function might not capture all dependencies
        accurately and may require additional refinement.

        This part of the code is a starting point and may need further
        improvements and customization.
    """
    top_level_directory = node_collection[root_node][0]
    for content_object in node_collection[top_level_directory]:
        if content_object.name == "requirements.txt":
            dependency_packages = []
            requirements_content = get_content_from_hashes(content_object.checksums)
            for line in requirements_content.splitlines():
                if line.strip():
                    dependency_packages.append(line.strip())
            return dependency_packages
    return None


def set_top_level_package(
    package_node: Node, node_collection: dict, metadata_node: Node
) -> Tuple[list, list, str]:
    """
    Creates a SPDX package instance of top level package
    and its relationship with the SPDX document

    Args:
        package_node (Node): directory node acting as top level package
        node_collection (dict): Collection of nodes found in the root directory,
            with keys as root-directory or sub-directories and value as a list of child nodes
            and also contains an extra key "METADATA_NODE" with value as the metadata file node
            which the tool currently supports
        metadata_node (Node): metadata node of top level package

    Returns:
        spdx_packages (list): list containing top level package as SPDX package
        spdx_package_relationships (list): list containing top level package
            relationship with SPDX document
        top_level_package.get_spdx_id() (str): SPDX id of top level package for
            creating relationships
    """
    spdx_packages = []
    spdx_relationships = []
    # Implementing Top Level Package
    if metadata_node:
        # If metadata_node is present
        top_level_package = TopLevelPackagePython(
            package_node=package_node,
            node_collection=node_collection,
            metadata_node=metadata_node,
        )
        spdx_package = Package(
            name=top_level_package.get_package_name(),
            spdx_id=top_level_package.get_spdx_id(),
            download_location=top_level_package.get_download_location(),
            version=top_level_package.get_version(),
            supplier=top_level_package.get_supplier(),
            files_analyzed=top_level_package.get_file_analyzed_status(),
            verification_code=top_level_package.get_verification_code(),
            license_concluded=top_level_package.get_license_concluded(),
            license_info_from_files=top_level_package.get_license_info_from_files(),
            license_declared=top_level_package.get_license_declared(),
        )
        spdx_relationship = Relationship(
            "SPDXRef-DOCUMENT",
            RelationshipType.DESCRIBES,
            top_level_package.get_spdx_id(),
        )
        spdx_packages.append(spdx_package)
        spdx_relationships.append(spdx_relationship)
    else:
        # If metadata_node is not present
        raise FileNotFoundError("Requested object doesn't contains metadata file!")

    return spdx_packages, spdx_relationships, top_level_package.get_spdx_id()


def set_dependency_packages(
    dependency_packages: list, top_level_package_spdx_id: str
) -> Tuple[list, list]:
    """
    Creates a SPDX package instance of dependency packages and their relationships

    Args:
        dependency_packages (dict): collection of dependency packages where key is package name
            and value is package version
        top_level_package_spdx_id (str): SPDX id of top level package for creating relationships

    Returns:
        spdx_packages (list): list of dependency packages as SPDX packages
        spdx_package_relationships (list): list contain relationships between
            various spdx elements with dependency packages
    """
    spdx_packages = []
    spdx_relationships = []
    if dependency_packages:
        for package in dependency_packages:
            dependency_package = DependencyPackagePython(package)
            spdx_package = Package(
                name=dependency_package.get_package_name(),
                spdx_id=dependency_package.get_spdx_id(),
                download_location=dependency_package.get_download_location(),
                files_analyzed=dependency_package.get_file_analyzed_status(),
                description=dependency_package.get_description(),
            )
            spdx_relationship = Relationship(
                top_level_package_spdx_id,
                RelationshipType.DEPENDS_ON,
                dependency_package.get_spdx_id(),
            )
            spdx_packages.append(spdx_package)
            spdx_relationships.append(spdx_relationship)

    return spdx_packages, spdx_relationships
