from swh.model.swhids import CoreSWHID, ObjectType
from swh.spdx.children import get_child


class Node:
    """Represents a content file or subdirectory node in the directory structure."""

    def __init__(
        self, name: str, swhid: CoreSWHID, path: str = "", checksums: dict = {}
    ):
        """
        Initialize a new instance of the Node class.

        Args:
            name (str): The name of the node.
            swhid (CoreSWHID): The Software Heritage CORE identifier of the node.
            path (str): The directory path of node object.
            checksums (str): The dictionary containing checksums of node object.
        """

        self.name = name
        self.swhid = swhid
        self.path = path
        self.is_directory = self.swhid.object_type == ObjectType.DIRECTORY
        self.checksums = checksums

    def get_children(self):
        """
        Retrieve the children nodes of the current directory node.

        Returns:
            dict: A dictionary of child nodes,
            where the keys are child names and the values is a list of swhid,
            checksums and directory path of child node.

        """
        if self.is_directory:
            return get_child(self.swhid, self.path)
        else:
            raise ValueError(f"{str(self.swhid)} is not a valid directory CoreSWHID")

    def set_path(self, node_properties: list):
        """
        Set the directory path of the node.

        Args:
            node_properties (list): list of swhid, checksums and directory path of the node

        Returns:
            None
        """
        self.path = node_properties[2]

    def set_checksums(self, node_properties: list):
        """
        Set the checksums of the node.

        Args:
            node_properties (list): list of swhid, checksums and directory path of the node

        Returns:
            None
        """
        if self.is_directory:
            self.checksums = {"sha1": node_properties[1]["id"]}
        else:
            self.checksums = node_properties[1]["hashes"]
