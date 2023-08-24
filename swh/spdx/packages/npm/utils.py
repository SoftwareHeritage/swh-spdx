from typing import Tuple

from spdx_tools.spdx.model import Package, Relationship, RelationshipType

from swh.spdx.node import Node
from swh.spdx.packages.npm.spdx_fields import DependencyPackageNPM, TopLevelPackageNPM


def get_dependency_packages(metadata_dict: dict) -> dict:
    """
    Detects dependencies of project

    Args:
        metadata_dict (dict): dictionary containing metadata entries extracted from
            metadata file "package.json"

    Returns:
        dependency_collection (dict): dictionary of collected dependencies where key is
            dependency name and value is corresponding version of dependency package
    """
    dependencies = metadata_dict.get("dependencies", {})
    peer_dependencies = metadata_dict.get("peerDependencies", {})
    dev_dependencies = metadata_dict.get("devDependencies", {})
    optional_dependencies = metadata_dict.get("optionalDependencies", {})
    # Combine dependencies
    all_dependencies = {
        **dependencies,
        **peer_dependencies,
        **dev_dependencies,
        **optional_dependencies,
    }
    dependency_collection = {}
    if all_dependencies:
        for package, version in all_dependencies.items():
            dependency_collection[package] = version
    return dependency_collection


def set_top_level_package(
    package_node: Node, node_collection: dict, metadata_node: Node
) -> Tuple[list, list, str, dict]:
    """
    Creates a SPDX package instance of top level packageand its relationship
    with the SPDX document

    Args:
        package_node (Node): directory node acting as top level package
        node_collection (dict): Collection of nodes found in the root directory,
            with keys as root-directory or sub-directories and value as a list of child nodes
            and also contains an extra key "METADATA_NODE" with value as the metadata file node
            which the tool currently supports
        metadata_node (Node): metadata node of top level package

    Returns:
        spdx_packages (list): list containing top level package as SPDX package
        spdx_package_relationships (list): list containing top level package relationship
            with SPDX document
        top_level_package.get_spdx_id() (str): SPDX id of top level package for creating
            relationships
        top_level_package.metadata_dict (dict): dictionary containing all metadata fields
            related to top_level_package extracted from its metadata file
    """
    spdx_packages = []
    spdx_package_relationships = []
    # Implementing Top Level Package
    if metadata_node:
        # If metadata_node is present
        top_level_package = TopLevelPackageNPM(
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
        spdx_package_relationship = Relationship(
            "SPDXRef-DOCUMENT",
            RelationshipType.DESCRIBES,
            top_level_package.get_spdx_id(),
        )
        spdx_packages.append(spdx_package)
        spdx_package_relationships.append(spdx_package_relationship)
    else:
        # If metadata_node is not present
        raise FileNotFoundError("Requested object doesn't contains metadata file!")

    return (
        spdx_packages,
        spdx_package_relationships,
        top_level_package.get_spdx_id(),
        top_level_package.metadata_dict,
    )


def set_dependency_packages(
    dependency_packages: dict, top_level_package_spdx_id: str
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
    spdx_package_relationships = []
    if dependency_packages:
        for package, version in dependency_packages.items():
            dependency_package = DependencyPackageNPM(
                dependency_package_name=package, dependency_package_version=version
            )
            spdx_package = Package(
                name=dependency_package.get_package_name(),
                version=dependency_package.get_version(),
                spdx_id=dependency_package.get_spdx_id(),
                download_location=dependency_package.get_download_location(),
                files_analyzed=dependency_package.get_file_analyzed_status(),
                description=dependency_package.get_description(),
            )
            spdx_package_relationship = Relationship(
                top_level_package_spdx_id,
                RelationshipType.DEPENDS_ON,
                dependency_package.get_spdx_id(),
            )
            spdx_packages.append(spdx_package)
            spdx_package_relationships.append(spdx_package_relationship)

    return spdx_packages, spdx_package_relationships
