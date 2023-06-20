from typing import Dict

from swh.spdx.children import get_child


class Node:
    """Represents a content file or subdirectory node in the directory structure."""

    def __init__(self, name, swhid) -> None:
        """
        Initialize a new instance of the Node class.

        Args:
            name (str): The name of the node.
            swhid (str): The Software Heritage identifier of the node.
        """

        self.name = name
        self.swhid = swhid
        self.path = ""
        self.checksums: Dict[str, str] = {}

    def is_directory(self) -> bool:
        """
        Check if the node represents a directory.

        Returns:
            bool: True if the node represents a directory, False otherwise.
        """
        return self.swhid.split(":")[2] == "dir"

    def get_children(self) -> Dict:
        """
        Retrieve the children nodes of the current directory node.

        Returns:
            dict: A dictionary of child nodes,
                  where the keys are child names and the values are SWHIDs.

        Raises:
            ValueError: If content object's swhid is passed to get_children()
        """
        if self.is_directory():
            return get_child(self.swhid)
        else:
            raise ValueError(f"{self.swhid}does not references to a directory object")

    def set_path(self, path_piece) -> None:
        """
        Set the path of the node.

        Args:
            path_piece (str): The path piece to append to the current path.

        Returns:
            None
        """
        if not self.path:
            separator = "/"
            self.path = separator.join([path_piece, self.name])

    def set_checksums(self, child_properties) -> None:
        """
        Set the checksums of the node.

        Args:
            child_properties (dict): The properties of the child node.

        Returns:
            None
        """
        if self.is_directory():
            self.checksums = {"sha1": child_properties[1]["id"]}
        else:
            self.checksums = child_properties[1]["hashes"]
