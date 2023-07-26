from datetime import datetime

from license_expression import get_spdx_licensing
from spdx_tools.spdx.model import (
    Actor,
    ActorType,
    Checksum,
    ChecksumAlgorithm,
    CreationInfo,
    PackagePurpose,
    PackageVerificationCode,
    SpdxNoAssertion,
)

from swh.spdx.content import get_content_from_hashes
from swh.spdx.node import Node
from swh.spdx.packages.verification_code import generate_verification_code


def get_metadata(node: Node) -> dict:
    """
    Parses the metadata file PKG-INFO

    Returns:
        metadata_dict (dict): dictionary with metadata_title eg. "License" as key
        and metadata eg "MIT" as value
    """
    if not node.name == "PKG-INFO":
        raise ValueError(f"{node.name} is not a expected metadata content object")
    text_content = get_content_from_hashes(node.checksums)
    metadata_dict = {}

    for line in text_content.splitlines():
        # TODO: Requires much more cleaner parshing
        if line.strip() and ": " in line.strip():  # Skip empty lines
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            metadata_dict[key] = value
    return metadata_dict


def set_creation_info(document_name: str) -> CreationInfo:
    """
    Contains information about the Tools and attributes used for creating SPDX document

    Args:
        document_name (str): Name of document

    Returns:
        creation_info (CreationInfo)
    """
    creation_info = CreationInfo(
        spdx_version="SPDX-2.3",
        spdx_id="SPDXRef-DOCUMENT",
        name=document_name,
        data_license="CC0-1.0",
        document_namespace="https://some.namespace",
        creators=[
            Actor(ActorType.ORGANIZATION, "SOFTWARE HERITAGE", "swh@example.com"),
            Actor(ActorType.TOOL, "swh-spdx"),
        ],
        created=datetime.now(),
    )
    return creation_info


class TopLevelPackage:
    """
    Class representing a Top level package object with
    methods to generate necessary spdx fields
    """

    def __init__(self, package_node: Node, metadata_node: Node, node_collection: dict):
        self.node_collection = node_collection
        self.package_node = package_node
        self.metadata_dict = get_metadata(metadata_node)

    def get_package_name(self) -> str:
        # Returns name of top-level package
        return self.package_node.name

    def get_spdx_id(self) -> str:
        # Returns a unique spdx id generated using path
        # for valid spdx id
        modified_path = (self.package_node.path).replace("/", "-")
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

    def get_version(self):
        # Returns version of python package
        if "Metadata-Version" in self.metadata_dict.keys():
            return self.metadata_dict["Metadata-Version"]
        return None

    def get_supplier(self):
        # Returns the supplier of python package
        if "Author" in self.metadata_dict.keys():
            if "Author-email" in self.metadata_dict.keys():
                author_email = self.metadata_dict["Author-email"]
            else:
                author_email = None
            return Actor(ActorType.PERSON, self.metadata_dict["Author"], author_email)
        return None

    def get_originator(self):
        # Returns the originator of python package
        return None

    def get_checksums(self):
        # Returns the sha1 checksum of directory treated as package
        return [Checksum(ChecksumAlgorithm.SHA1, self.package_node.checksums["sha1"])]

    def get_license_concluded(self):
        # Returns license concluded by the Author of project
        try:
            # TODO: Requires cleaner checking of valid spdx licenses
            if "License" in self.metadata_dict.keys():
                if self.metadata_dict["License"] == "UNKNOWN":
                    raise Exception("Unknown error")
                return get_spdx_licensing().parse(self.metadata_dict["License"])
        except Exception:
            # When no License is specified or parsing of license is unsuccessful
            return SpdxNoAssertion()

    def get_license_info_from_files(self):
        # TODO: Parse Licensing info from files in the package
        return None

    def get_license_declared(self):
        # TODO: Parse licenses declared by Author in the package
        return SpdxNoAssertion()

    def get_description(self):
        if "Description" in self.metadata_dict.keys():
            return self.metadata_dict["Description"]
        return None

    def get_primary_package_purpose(self):
        # Currently assuming the purpose purpose as LIBRARY
        return PackagePurpose.LIBRARY

    def get_download_location(self):
        # Returns download url of package
        if "Download-URL" in self.metadata_dict.keys():
            return self.metadata_dict["Download-URL"]
        return SpdxNoAssertion()


class DependencyPackage:
    """
    Class representing Dependency package object
    with methods to generate necessary spdx fields
    """

    def __init__(self, dependency_package_name: str):
        self.package_name = dependency_package_name

    def get_package_name(self) -> str:
        # Returns package name
        return self.package_name

    def get_spdx_id(self) -> str:
        # Returns unique spdx id of package
        return f"SPDXRef-{self.package_name}"

    def get_download_location(self):
        # TODO: Get download location of dependency found
        return None

    def get_file_analyzed_status(self) -> bool:
        # Files in Dependency package are not analyzed therefore False
        return False

    def get_description(self):
        # TODO: Extract description of dependency
        return None
