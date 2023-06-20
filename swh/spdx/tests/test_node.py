import unittest
from unittest.mock import patch

from swh.spdx.node import Node


class NodeTestCase(unittest.TestCase):
    """
    Test case for the Node class.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.directory_node = Node(
            name="rfcreader",
            swhid="swh:1:dir:de0f1edd306d6e9fc67ddf9b741aa7b9954e21d9",  # noqa
        )
        self.content_node = Node(
            name="rfcreader.py",
            swhid="swh:1:cnt:d057105f2bea6b982e6c526cab5dee920a6ee02b",
        )

    def tearDown(self):
        """
        Clean up any resources used in the tests.
        """
        pass

    def test_is_directory(self):
        """
        Test the `is_directory` method.
        """
        self.assertTrue(self.directory_node.is_directory())
        self.assertFalse(self.content_node.is_directory())

    @patch("swh.spdx.children.get_child")
    def test_get_children(self, mock_get_child):
        """
        Test the `get_children` method.
        """
        # Set up mock response
        mock_response = {
            "rfcreader.py": [
                "swh:1:cnt:d057105f2bea6b982e6c526cab5dee920a6ee02b",
                {
                    "hashes": {
                        "sha1": "880c85189ab5ed96965e2f965077591758f6c554",
                        "sha256": "2c5bd52b5d4a1c81f1e2946bcce1d6d4ee1cad977c5bde38f9a9be0f7dff6ffb",  # noqa
                    }
                },
            ],
            "__init__.py": [
                "swh:1:cnt:9342afd2b62ac51f08ef8100c2c97ad394ce0962",
                {
                    "hashes": {
                        "sha1": "3562c8b75183ff91301038025d7607f409106f4d",
                        "sha256": "89130d1e8c203b273afee095681260d34d5d534686ea8d414b03b504325fdf2f",  # noqa
                    }
                },
            ],
        }
        mock_get_child.return_value = mock_response
        # Test get_children() method on directory_node
        result = self.directory_node.get_children()
        self.assertEqual(result, mock_response)
        # Test get_children() method on content_node
        with self.assertRaises(ValueError):
            result = self.content_node.get_children()

    def test_set_path(self):
        """
        Test the `set_path` method.
        """
        self.directory_node.set_path("")
        self.assertEqual("/rfcreader", self.directory_node.path)

        self.content_node.set_path("/rfcreader")
        self.assertEqual("/rfcreader/rfcreader.py", self.content_node.path)

    def test_set_checksums(self):
        """
        Test the `set_checksums` method.
        """
        child_properties = [
            "swh:1:dir:de0f1edd306d6e9fc67ddf9b741aa7b9954e21d9",
            {"id": "de0f1edd306d6e9fc67ddf9b741aa7b9954e21d9"},
        ]

        self.directory_node.set_checksums(child_properties)
        expected_result = {"sha1": "de0f1edd306d6e9fc67ddf9b741aa7b9954e21d9"}
        self.assertEqual(expected_result, self.directory_node.checksums)

        child_properties = [
            "swh:1:cnt:d057105f2bea6b982e6c526cab5dee920a6ee02b",
            {
                "hashes": {
                    "sha1": "880c85189ab5ed96965e2f965077591758f6c554",
                    "sha256": "2c5bd52b5d4a1c81f1e2946bcce1d6d4ee1cad977c5bde38f9a9be0f7dff6ffb",  # noqa
                }
            },
        ]
        self.content_node.set_checksums(child_properties)
        expected_result = {
            "sha1": "880c85189ab5ed96965e2f965077591758f6c554",
            "sha256": "2c5bd52b5d4a1c81f1e2946bcce1d6d4ee1cad977c5bde38f9a9be0f7dff6ffb",  # noqa
        }
        self.assertEqual(expected_result, self.content_node.checksums)


if __name__ == "__main__":
    unittest.main()
