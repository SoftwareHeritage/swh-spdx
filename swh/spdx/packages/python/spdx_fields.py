from license_expression import get_spdx_licensing
from spdx_tools.spdx.model import Actor, ActorType, SpdxNoAssertion

from swh.spdx.content import get_content_from_hashes
from swh.spdx.node import Node
from swh.spdx.packages.base import TopLevelPackage


class TopLevelPackagePython(TopLevelPackage):
    """
    Class representing a Top level package object with
    methods to generate necessary spdx fields
    """

    def __init__(self, package_node: Node, node_collection: dict, metadata_node: Node):
        super().__init__(package_node=package_node, node_collection=node_collection)
        self.metadata_dict = self.get_metadata_dict(metadata_node)

    def get_metadata_dict(self, node: Node) -> dict:
        """
        Parsing the metadata file PKG-INFO

        Returns:
            metadata_dict (dict): dictionary with metadata_title eg. "License" as key
                and metadata eg "MIT" as value
        """
        if node.name != "PKG-INFO":
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

    def get_version(self):
        """
        Returns version of python package
        """
        return self.metadata_dict.get("Metadata-Version")

    def get_supplier(self):
        """
        Returns the supplier of python package
        """
        if "Author" in self.metadata_dict.keys():
            if "Author-email" in self.metadata_dict.keys():
                author_email = self.metadata_dict["Author-email"]
            else:
                author_email = None
            return Actor(ActorType.PERSON, self.metadata_dict["Author"], author_email)
        return None

    def get_originator(self):
        """
        Returns the originator of python package

        Note: Not currently implemented due to ambiguity between the identification of
              supplier and originator of package from the metadata file

              Supplier: The actual distribution source for the package/directory identified in
              the SPDX document. This might or might not be different from the originating
              distribution source for the package

              Originator: If the package identified in the SPDX document originated from a
              different person or organization than identified as Package Supplier, this
              field identifies from where or whom the package originally came
        """
        return None

    def get_license_concluded(self):
        """
        Returns license concluded by the Author of project
        """
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
        """
        TODO: Parse Licensing info from files in the package

        Note: This part of the code is not yet implemented due to compexity in
              scanning the headers of source files and extracting the license used in
              each individual file but can be implemented in future.
        """
        return None

    def get_license_declared(self):
        """
        TODO: Parse licenses declared by Author in the package

        Note: May require the implementation of get_license_info_from_files
              function to extract the licenses declared by the author of package,
              will not include licenses not originated from the package author.
        """
        return SpdxNoAssertion()

    def get_description(self):
        """
        Returns the description of python package
        """
        return self.metadata_dict.get("Description")

    def get_download_location(self):
        """
        Returns download url of package
        """
        if "Download-URL" in self.metadata_dict:
            return self.metadata_dict["Download-URL"]
        return SpdxNoAssertion()


class DependencyPackagePython:
    """
    Class representing Dependency package object
    with methods to generate necessary spdx fields

    Note: For now this class will only get instantiated when the get_dependency_packages
          function detects dependencies which currently only collect dependencies from
          "requirements.txt" file therefore needs improvement
    """

    def __init__(self, dependency_package_name: str):
        self.package_name = dependency_package_name

    def get_package_name(self) -> str:
        """
        Returns package name
        """
        return self.package_name

    def get_spdx_id(self) -> str:
        """
        Returns unique spdx id of package
        """
        return f"SPDXRef-{self.package_name}"

    def get_download_location(self):
        """
        TODO: Get download location of dependency found

        Note: Requires extracting the dependency package's information.
              This code is not currently implemented.

              "importlib-metadata" package can be considered for the implementation in future
        """
        return SpdxNoAssertion()

    def get_file_analyzed_status(self) -> bool:
        """
        Files in Dependency package are not analyzed therefore False

        Note: False because we are not analysing the source files of dependency package
        """
        return False

    def get_description(self):
        """
        TODO: Extract description of dependency

        Note: Requires the dependency package's information, not yet implemented but
              can be implemented in future
        """
        return None
