from spdx_tools.spdx.model import (
    Checksum,
    ChecksumAlgorithm,
    File,
    PackagePurpose,
    PackageVerificationCode,
    Relationship,
    RelationshipType,
    SpdxNoAssertion,
)

from swh.spdx.node import Node
from swh.spdx.packages.verification_code import generate_verification_code


class TopLevelPackage:
    """
    Class representing a Top level package object with
    methods to generate necessary spdx fields
    """

    def __init__(self, package_node: Node, node_collection: dict):
        self.node_collection = node_collection
        self.package_node = package_node

    def get_package_name(self) -> str:
        # Returns name of top-level package
        return self.package_node.name

    def get_spdx_id(self) -> str:
        # Returns a unique spdx id generated using path
        # for valid spdx id
        modified_path = (self.package_node.path).replace("/", "-").replace("_", "-")
        return f"SPDXRef-{modified_path}"

    def get_file_analyzed_status(self) -> bool:
        # True status for analyzing all files in top-level package
        return True

    def get_verification_code(self) -> PackageVerificationCode:
        # Returns Unique Verification Code of package
        # generated using the algorithm specified by SPDX
        list_of_files_of_package = self.node_collection[self.package_node]
        package_verification_code = generate_verification_code(list_of_files_of_package)
        return package_verification_code

    def get_checksums(self):
        # Returns the sha1 checksum of directory treated as package
        return [Checksum(ChecksumAlgorithm.SHA1, self.package_node.checksums["sha1"])]

    def get_primary_package_purpose(self):
        # Currently assuming the purpose purpose as LIBRARY
        return PackagePurpose.LIBRARY


class PackageFile:
    """
    Class representing a dependency package object with
    methods to generate necessary spdx fields
    """

    def __init__(self, content_node: Node):
        self.file_node = content_node

    def get_name(self):
        return self.file_node.name

    def get_spdx_id(self):
        modified_path = (self.file_node.path).replace("/", "-").replace("_", "-")
        return f"SPDXRef-{modified_path}"

    def get_checksums(self):
        return [Checksum(ChecksumAlgorithm.SHA1, self.file_node.checksums["sha1"])]

    def get_license_concluded(self):
        return SpdxNoAssertion()


def set_files(node_collection: dict, top_level_package_spdx_id: str):
    """
    Creates the SPDX File instance of files in a top level package

    Args:
        node_collection (dict): Collection of nodes found in the root directory,
            with keys as root-directory or sub-directories and value as a list of child nodes
        top_level_package_spdx_id (str): SPDX id of top level package for creating relationships

    Returns:
        spdx_files (list): list of files as spdx file
        spdx_file_relationships (list): list containing relationship between files and top
            level package
    """
    spdx_files = []
    spdx_file_relationships = []
    for directory_node, file_nodes in node_collection.items():
        for file_node in file_nodes:
            if not file_node.is_directory:
                file = PackageFile(content_node=file_node)
                spdx_file = File(
                    name=file.get_name(),
                    spdx_id=file.get_spdx_id(),
                    checksums=file.get_checksums(),
                    license_concluded=file.get_license_concluded(),
                )
                spdx_file_relationship = Relationship(
                    top_level_package_spdx_id,
                    RelationshipType.CONTAINS,
                    file.get_spdx_id(),
                )
                spdx_files.append(spdx_file)
                spdx_file_relationships.append(spdx_file_relationship)
    return spdx_files, spdx_file_relationships
