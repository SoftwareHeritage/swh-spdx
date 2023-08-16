import json

from license_expression import get_spdx_licensing
from spdx_tools.spdx.model import Actor, ActorType, SpdxNoAssertion

from swh.spdx.content import get_content_from_hashes
from swh.spdx.node import Node
from swh.spdx.packages.base import TopLevelPackage


def get_metadata_npm(node: Node) -> dict:
    """
    Parses the metadata file PKG-INFO

    Returns:
        metadata_dict (dict): dictionary with metadata_title eg. "License" as key
        and metadata eg "MIT" as value
    """
    if not node.name == "package.json":
        raise ValueError(f"{node.name} is not a expected metadata content object")
    text_content = get_content_from_hashes(node.checksums)
    metadata_dict = json.loads(text_content)
    return metadata_dict


class TopLevelPackageNPM(TopLevelPackage):
    """
    Class representing a Top level package object with
    methods to generate necessary spdx fields
    """

    def __init__(self, package_node: Node, metadata_node: Node, node_collection: dict):
        super().__init__(package_node=package_node, node_collection=node_collection)
        self.metadata_dict = get_metadata_npm(metadata_node)

    def get_version(self):
        # Returns version of python package
        if "version" in self.metadata_dict.keys():
            return self.metadata_dict["version"]
        return None

    def get_supplier(self):
        # Returns the supplier of python package
        if "author" in self.metadata_dict.keys():
            return Actor(ActorType.PERSON, self.metadata_dict["author"])
        return None

    def get_originator(self):
        # Returns the originator of python package
        return None

    def get_license_concluded(self):
        # Returns license concluded by the Author of project
        try:
            # TODO: Requires cleaner checking of valid spdx licenses
            if "license" in self.metadata_dict.keys():
                return get_spdx_licensing().parse(self.metadata_dict["license"])
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
        if "description" in self.metadata_dict.keys():
            return self.metadata_dict["description"]
        return None

    def get_download_location(self):
        # Returns download url of package
        return SpdxNoAssertion()


class DependencyPackageNPM:
    """
    Class representing Dependency package object
    with methods to generate necessary spdx fields
    """

    def __init__(self, dependency_package_name: str, dependency_package_version: str):
        self.package_name = dependency_package_name
        self.version = dependency_package_version

    def get_version(self) -> str:
        # Returns package version
        return self.version

    def get_package_name(self) -> str:
        # Returns package name
        return self.package_name

    def get_spdx_id(self) -> str:
        # Returns unique spdx id of package
        return f"SPDXRef-{self.package_name}"

    def get_download_location(self):
        # TODO: Get download location of dependency found
        return SpdxNoAssertion()

    def get_file_analyzed_status(self) -> bool:
        # Files in Dependency package are not analyzed therefore False
        return False

    def get_description(self):
        # TODO: Extract description of dependency
        return None
