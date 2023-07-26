from spdx_tools.spdx.model import Document, Package, Relationship, RelationshipType
from spdx_tools.spdx.writer.write_anything import write_file

from swh.model.swhids import CoreSWHID
from swh.spdx.content import get_content_from_hashes
from swh.spdx.node import Node
from swh.spdx.packages.python.spdx_fields import (
    DependencyPackage,
    TopLevelPackage,
    set_creation_info,
)
from swh.spdx.traverse import traverse_root


def get_metadata_node(node_collection: dict):
    """
    Detects the metadata node in the top level package directory

    Args:
    node_collection (dict): Collection of nodes found in the root directory,
    with keys as root-directory or sub-directories and value as a list of child nodes

    Returns:
        content_object (Node): metadata node
    """
    top_level_directory = list(node_collection.keys())[1]
    for content_object in node_collection[top_level_directory]:
        if content_object.name == "PKG-INFO":
            return content_object
    raise Exception("Metadata File not found!")


def get_dependency_packages(node_collection: dict):
    """
    Detects dependencies of project

    Args:
        node_collection (dict): Collection of nodes found in the root directory,
        with keys as root-directory or sub-directories and value as a list of child nodes

    Returns:
        dependency_packages (list): list of detected dependencies
    """
    top_level_directory = list(node_collection.keys())[1]
    for content_object in node_collection[top_level_directory]:
        if content_object.name == "requirements.txt":
            dependency_packages = []
            requirements_content = get_content_from_hashes(content_object.checksums)
            for line in requirements_content.splitlines():
                if line.strip():
                    dependency_packages.append(line.strip())
            return dependency_packages
    return None


def generate_spdx(root_swhid: CoreSWHID):
    """
    Generates the spdx document and writes it in the current directory

    Args:
        root_swhid (CoreSWHID): swhid of root directory
    """
    # Assuming the root directory as ./ specified by the SPDX specification
    root_node = Node(name=".", swhid=root_swhid)
    node_collection = traverse_root(node=root_node, first_iteration=True)
    top_level_package_node = list(node_collection.keys())[1]
    creation_info = set_creation_info(top_level_package_node.name)
    spdx_document = Document(creation_info)
    metadata_node = get_metadata_node(node_collection)
    if metadata_node:
        # If metadata_node is present
        top_level_package = TopLevelPackage(
            package_node=top_level_package_node,
            node_collection=node_collection,
            metadata_node=metadata_node,
        )
        pkg = Package(
            name=top_level_package.get_package_name(),
            spdx_id=top_level_package.get_spdx_id(),
            download_location=top_level_package.get_download_location(),
            version=top_level_package.get_version(),
            supplier=top_level_package.get_supplier(),
            files_analyzed=top_level_package.get_file_analyzed_status(),
            verification_code=top_level_package.get_verification_code(),
            checksums=top_level_package.get_checksums(),
            license_concluded=top_level_package.get_license_concluded(),
            license_info_from_files=top_level_package.get_license_info_from_files(),
            license_declared=top_level_package.get_license_declared(),
        )
        spdx_document.packages = [pkg]
        spdx_document.relationships = [
            Relationship(
                "SPDXRef-DOCUMENT",
                RelationshipType.DESCRIBES,
                top_level_package.get_spdx_id(),
            )
        ]
    else:
        # If metadata_node is not present
        raise FileNotFoundError("Requested object doesn't contains metadata file!")
    dependency_packages = get_dependency_packages(node_collection)
    if dependency_packages:
        for package in dependency_packages:
            dependency_package = DependencyPackage(package)
            pkg = Package(
                name=dependency_package.get_package_name(),
                spdx_id=dependency_package.get_spdx_id(),
                download_location=dependency_package.get_download_location(),
                files_analyzed=dependency_package.get_file_analyzed_status(),
                description=dependency_package.get_description(),
            )
            spdx_document.packages = [pkg]
            spdx_document.relationships = [
                Relationship(
                    top_level_package.get_spdx_id(),
                    RelationshipType.DEPENDS_ON,
                    dependency_package.get_spdx_id(),
                )
            ]
    # Writes the spdx document in the current directory
    write_file(spdx_document, "my_spdx_document3.spdx.json")
