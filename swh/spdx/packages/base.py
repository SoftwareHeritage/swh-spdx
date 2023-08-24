import re

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
        """
        Returns name of top-level package
        """
        return self.package_node.name

    def get_spdx_id(self) -> str:
        """
        Returns a unique spdx id generated using path for valid spdx id
        """
        modified_path = generate_unique_id(self.package_node.path)
        return f"SPDXRef-{modified_path}"

    def get_file_analyzed_status(self) -> bool:
        """
        File analysed status is True as all the files are analysed for checksums though requires
        implementation for licenses used
        """
        return True

    def get_verification_code(self) -> PackageVerificationCode:
        """
        Returns Unique Verification Code of package generated using the algorithm specified
        by SPDX
        """
        list_of_files_of_package = self.node_collection[self.package_node]
        package_verification_code = generate_verification_code(list_of_files_of_package)
        return package_verification_code

    def get_primary_package_purpose(self):
        """
        Currently assuming the purpose purpose as LIBRARY
        """
        return PackagePurpose.LIBRARY


class PackageFile:
    """
    Class representing a file object with
    methods to generate necessary spdx fields
    """

    def __init__(self, content_node: Node):
        self.file_node = content_node

    def get_name(self) -> str:
        """
        Returns the name of file node
        """
        return self.file_node.name

    def get_spdx_id(self) -> str:
        """
        Returns a unique spdx id generated using name of file for valid spdx id
        """
        modified_path = generate_unique_id(self.file_node.path)
        return f"SPDXRef-{modified_path}"

    def get_checksums(self):
        """
        Returns the checksums of file node
        """
        return [Checksum(ChecksumAlgorithm.SHA1, self.file_node.checksums["sha1"])]

    def get_license_concluded(self):
        """
        Returns the license concluded in the file object

        Note: Not yet implemented but can be implemented in future using the
              methadology of scanning the header of file
        """
        return SpdxNoAssertion()


def set_files(node_collection: dict, top_level_package_spdx_id: str):
    """Creates the SPDX File instance of files in a top level package

    Args:
        node_collection (dict): Collection of nodes found in the root directory,
            with keys as root-directory or sub-directories and value as a list of child nodes
            and also contains an extra key "METADATA_NODE" with value as the metadata file node
            which the tool currently supports
        top_level_package_spdx_id (str): SPDX id of top level package for creating relationships

    Returns:
        spdx_files (list): list of files as spdx file
        spdx_file_relationships (list): list containing relationship between files and top
            level package
    """
    spdx_files = []
    spdx_file_relationships = []
    for directory_node, file_nodes in node_collection.items():
        # Checking that directory node is in fact a node and not the "METADATA_NODE" key
        if isinstance(directory_node, Node):
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


def get_metadata_node(node_collection: dict) -> Node:
    """
    Detects the metadata node in the top level package directory

    Args:
        node_collection (dict): Collection of nodes found in the root directory,
            with keys as root-directory or sub-directories and value as a list of child nodes
            and also contains an extra key "METADATA_NODE" with value as the metadata file node
            which the tool currently supports

    Returns:
        content_object (Node): metadata node
    """
    if "METADATA_NODE" in node_collection:
        return node_collection["METADATA_NODE"]
    raise Exception("Metadata File not found!")


def generate_unique_id(file_path) -> str:
    """
    Generates a unquie id using directory path of object for creating spdx id
    """
    # Replace non-alphanumeric characters with "-"
    sanitized_path = re.sub(r"[^a-zA-Z0-9.-]", "-", file_path)
    # Remove consecutive "-" characters
    unique_id = re.sub(r"-+", "-", sanitized_path)
    # Remove leading and trailing "-"
    unique_id = unique_id.strip("-")
    return unique_id
