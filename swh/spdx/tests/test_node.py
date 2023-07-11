from unittest.mock import patch

import pytest

from swh.model.swhids import CoreSWHID, ObjectType
from swh.spdx.node import Node


@pytest.fixture
def sample_directory_node():
    """
    Test case for directory node with path =""
    will act as a root directory.
    """
    directory_node = Node(
        name="rfcreader",
        swhid=CoreSWHID(
            object_type=ObjectType.DIRECTORY,
            object_id=bytes.fromhex("de0f1edd306d6e9fc67ddf9b741aa7b9954e21d9"),
        ),
    )
    return directory_node


@pytest.fixture
def sample_directory_node_with_preset_path():
    """
    test case for directory node with preset path
    will act as a subdirectory.
    """
    directory_node = Node(
        name="rfcreader",
        swhid=CoreSWHID(
            object_type=ObjectType.DIRECTORY,
            object_id=bytes.fromhex("de0f1edd306d6e9fc67ddf9b741aa7b9954e21d9"),
        ),
        path="rfcreader-0.4/rfcreader",
    )
    return directory_node


@pytest.fixture
def sample_content_node():
    """
    test case for content node with preset path.
    """
    content_node = Node(
        name="rfcreader.py",
        swhid=CoreSWHID(
            object_type=ObjectType.CONTENT,
            object_id=bytes.fromhex("d057105f2bea6b982e6c526cab5dee920a6ee02b"),
        ),
        path="rfcreader-0.4/rfcreader/rfcreader.py",
    )
    return content_node


@pytest.fixture
def sample_directory_node_properties():
    """
    test case for directory node properties.
    """
    directory_node_properties = [
        CoreSWHID(
            object_type=ObjectType.DIRECTORY,
            object_id=bytes.fromhex("de0f1edd306d6e9fc67ddf9b741aa7b9954e21d9"),
        ),
        {"id": "de0f1edd306d6e9fc67ddf9b741aa7b9954e21d9"},
        "rfcreader-0.4/rfcreader",
    ]
    return directory_node_properties


@pytest.fixture
def sample_content_node_properties():
    """
    test case for content node properties.
    """
    content_node_properties = [
        CoreSWHID(
            object_type=ObjectType.CONTENT,
            object_id=bytes.fromhex("d057105f2bea6b982e6c526cab5dee920a6ee02b"),
        ),
        {
            "hashes": {
                "sha1": "880c85189ab5ed96965e2f965077591758f6c554",
                "sha256": "2c5bd52b5d4a1c81f1e2946bcce1d6d4ee1cad977c5bde38f9a9be0f7dff6ffb",
                "sha1_git": "d057105f2bea6b982e6c526cab5dee920a6ee02b",
                "blake2s256": "c16e47ecfc279bb595443bcf2fb40d88c5e755be15a7d4bc377ea9dc5b313134",  # noqa
            }
        },
        "rfcreader-0.4/rfcreader/rfcreader.py",
    ]
    return content_node_properties


def test_is_directory(sample_content_node: Node, sample_directory_node: Node):
    """
    Test the `is_directory` method.
    """
    assert sample_directory_node.is_directory is True
    assert sample_content_node.is_directory is False


@patch("swh.spdx.node.get_child")
def test_get_children_on_directory_object(
    mock_get_child, sample_directory_node_with_preset_path: Node
):
    """
    Test the `get_children` method on directory node.
    """
    # Set up mock response

    mock_response = {
        "rfcreader.py": [
            CoreSWHID(
                object_type=ObjectType.CONTENT,
                object_id=bytes.fromhex("d057105f2bea6b982e6c526cab5dee920a6ee02b"),
            ),
            {
                "hashes": {
                    "sha1": "880c85189ab5ed96965e2f965077591758f6c554",
                    "sha256": "2c5bd52b5d4a1c81f1e2946bcce1d6d4ee1cad977c5bde38f9a9be0f7dff6ffb",  # noqa
                    "sha1_git": "d057105f2bea6b982e6c526cab5dee920a6ee02b",
                    "blake2s256": "c16e47ecfc279bb595443bcf2fb40d88c5e755be15a7d4bc377ea9dc5b313134",  # noqa
                }
            },
            "rfcreader-0.4/rfcreader/rfcreader.py",
        ],
        "__init__.py": [
            CoreSWHID(
                object_type=ObjectType.CONTENT,
                object_id=bytes.fromhex("9342afd2b62ac51f08ef8100c2c97ad394ce0962"),
            ),
            {
                "hashes": {
                    "sha1": "3562c8b75183ff91301038025d7607f409106f4d",
                    "sha256": "89130d1e8c203b273afee095681260d34d5d534686ea8d414b03b504325fdf2f",  # noqa
                    "sha1_git": "9342afd2b62ac51f08ef8100c2c97ad394ce0962",
                    "blake2s256": "87a7d0efbda5b12809d81a270bd7c973bfb96d8240fb7934937c5aa77eb9ac4a",  # noqa
                }
            },
            "rfcreader-0.4/rfcreader/__init__.py",
        ],
    }

    mock_get_child.return_value = mock_response
    response = sample_directory_node_with_preset_path.get_children()

    assert response == mock_response


def test_get_children_on_content_object(sample_content_node: Node):
    """
    Test the `get_children` method on content node
    """
    with pytest.raises(ValueError):
        sample_content_node.get_children()


def test_set_path(
    sample_directory_node: Node,
    sample_directory_node_properties: list,
    sample_content_node: Node,
    sample_content_node_properties: list,
):
    """
    Test the `set_path` method on directory node and content node.
    """
    sample_directory_node.set_path(sample_directory_node_properties)
    sample_content_node.set_path(sample_content_node_properties)
    assert sample_directory_node.path == "rfcreader-0.4/rfcreader"
    assert sample_content_node.path == "rfcreader-0.4/rfcreader/rfcreader.py"


def test_set_checksums(
    sample_directory_node: Node,
    sample_directory_node_properties: list,
    sample_content_node: Node,
    sample_content_node_properties: list,
):
    """
    Test the `set_checksums` method on directory node and content node.
    """
    sample_directory_node.set_checksums(sample_directory_node_properties)
    sample_content_node.set_checksums(sample_content_node_properties)

    assert sample_directory_node.checksums == {
        "sha1": "de0f1edd306d6e9fc67ddf9b741aa7b9954e21d9"
    }
    assert sample_content_node.checksums == {
        "sha1": "880c85189ab5ed96965e2f965077591758f6c554",
        "sha256": "2c5bd52b5d4a1c81f1e2946bcce1d6d4ee1cad977c5bde38f9a9be0f7dff6ffb",
        "sha1_git": "d057105f2bea6b982e6c526cab5dee920a6ee02b",
        "blake2s256": "c16e47ecfc279bb595443bcf2fb40d88c5e755be15a7d4bc377ea9dc5b313134",
    }
