from unittest.mock import patch

import pytest

from swh.spdx.node import Node
from swh.spdx.tests.utils import assert_node
from swh.spdx.traverse import traverse_root

SAMPLE_ROOT_DIRECTORY_STRUCTURE = {
    "swhid": "swh:1:dir:7b717af4625b75db3d10709cefcdb620751ec186",
    "name": "ipython-cosmos-0.1.5",
    "children": {
        "README.md": "ipython-cosmos-0.1.5/README.md",
        "cosmos_sql": "ipython-cosmos-0.1.5/cosmos_sql",
        "PKG-INFO": "ipython-cosmos-0.1.5/PKG-INFO",
        "PKG-INFO": "ipython-cosmos-0.1.5/PKG-INFO",
        "setup.py": "ipython-cosmos-0.1.5/setup.py",
        "LICENSE.txt": "ipython-cosmos-0.1.5/LICENSE.txt",
    },
    "sub_directories_with_children": {
        "cosmos_sql": {
            "__init__.py": "ipython-cosmos-0.1.5/cosmos_sql/__init__.py",
            "VERSION": "ipython-cosmos-0.1.5/cosmos_sql/VERSION",
        },
    },
}


@pytest.fixture
def sample_node_collection():
    """
    Collection of nodes found in the root directory,
    with keys as root-directory or sub-directories and value as a list of child nodes
    """
    NODE_COLLECTION_OF_SAMPLE_ROOT_DIRECTORY = {
        Node(
            name="ipython-cosmos-0.1.5",
            swhid="swh:1:dir:7b717af4625b75db3d10709cefcdb620751ec186",
            path="ipython-cosmos-0.1.5",
        ): [
            Node(
                name="README.md",
                swhid="swh:1:cnt:791ff53442a421a68ff9db2e808522adfc4d93ca",
                path="ipython-cosmos-0.1.5/README.md",
                checksums={
                    "sha1": "5e36830e75ea751e8d1323f4c5bdbfdd0143bdca",
                    "sha256": "7936ae3d6ce0d039223a2fc51c6a6c2ff17e114abf59d0e3e93cc3221dc2161a",  # noqa
                },
            ),
            Node(
                name="cosmos_sql",
                swhid="swh:1:dir:504251e6894262e5f9c603a7178042e4034dfdc3",
                path="ipython-cosmos-0.1.5/cosmos_sql",
                checksums={
                    "sha1": "504251e6894262e5f9c603a7178042e4034dfdc3",
                },
            ),
            Node(
                name="PKG-INFO",
                swhid="swh:1:cnt:bce1e1f42d45a425b828abf2e3b7c45cda6188ca",
                path="ipython-cosmos-0.1.5/PKG-INFO",
                checksums={
                    "sha1": "b1d809a97e3139f9a9d2890551e5dd448b541202",
                    "sha256": "4a15bc736fbf8a7f9cdeb7b74038d7e033ed0990690c4fc609406cdd8e5f73e9",  # noqa
                },
            ),
            Node(
                name="setup.py",
                swhid="swh:1:cnt:b1e56aad066fcff343882e830cefd0ce082f0ccf",
                path="ipython-cosmos-0.1.5/setup.py",
                checksums={
                    "sha1": "31388c09456c2cb0a741d60c3ca26e5a9b6facbf",
                    "sha256": "51af40f2a7a43c60538d59368671df3f6fb4cd394a7c219bf4c6b20fde4d334c",  # noqa
                },
            ),
            Node(
                name="LICENSE.txt",
                swhid="swh:1:cnt:05058cca5546507ced02bad620cb7b856ebf5f63",
                path="ipython-cosmos-0.1.5/LICENSE.txt",
                checksums={
                    "sha1": "0ec04e5f1e1826931ef4f9446dc0009b41224d1f",
                    "sha256": "55c3b9c2351473c9e61a5b326f631261fd4cb50eec2a7eef750df6ca45150732",  # noqa
                },
            ),
        ],
        Node(
            name="cosmos_sql",
            swhid="swh:1:dir:504251e6894262e5f9c603a7178042e4034dfdc3",
            path="ipython-cosmos-0.1.5/cosmos_sql",
            checksums={
                "sha1": "504251e6894262e5f9c603a7178042e4034dfdc3",
            },
        ): [
            Node(
                name="__init__.py",
                swhid="swh:1:cnt:aa4046a1143322e93dd86f40861fa0be0b08f07e",
                path="ipython-cosmos-0.1.5/cosmos_sql/__init__.py",
                checksums={
                    "sha1": "978187e0361b2674dbbdd47c824a5e0e5a80c614",
                    "sha256": "9bbe64a2168837d0bbee62f1734077ad3053b6661f8c9b0c9093bdf0224cf183",  # noqa
                },
            ),
            Node(
                name="VERSION",
                swhid="swh:1:cnt:9faa1b7a7339db85692f91ad4b922554624a3ef7",
                path="ipython-cosmos-0.1.5/cosmos_sql/VERSION",
                checksums={
                    "sha1": "77ba406cbdaa641f1f4ca09902edf5f03a0e0a1e",
                    "sha256": "800cf1c0392b24de7c0a1c6ea6778ecb433dec71c49a150bce96a98477527b2f",  # noqa
                },
            ),
        ],
    }
    return NODE_COLLECTION_OF_SAMPLE_ROOT_DIRECTORY


@patch("swh.spdx.node.get_child")
def test_traverse_root_success(mock_get_child, sample_node_collection):
    """
    Tests the traverse_root function over the sample root directory
    """
    mock_get_child.side_effect = [
        # First response is child details of sample_root_directory
        {
            "README.md": [
                "swh:1:cnt:791ff53442a421a68ff9db2e808522adfc4d93ca",
                {
                    "hashes": {
                        "sha1": "5e36830e75ea751e8d1323f4c5bdbfdd0143bdca",
                        "sha256": "7936ae3d6ce0d039223a2fc51c6a6c2ff17e114abf59d0e3e93cc3221dc2161a",  # noqa
                    }
                },
                "ipython-cosmos-0.1.5/README.md",
            ],
            "cosmos_sql": [
                "swh:1:dir:504251e6894262e5f9c603a7178042e4034dfdc3",
                {"id": "504251e6894262e5f9c603a7178042e4034dfdc3"},
                "ipython-cosmos-0.1.5/cosmos_sql",
            ],
            "PKG-INFO": [
                "swh:1:cnt:bce1e1f42d45a425b828abf2e3b7c45cda6188ca",
                {
                    "hashes": {
                        "sha1": "b1d809a97e3139f9a9d2890551e5dd448b541202",
                        "sha256": "4a15bc736fbf8a7f9cdeb7b74038d7e033ed0990690c4fc609406cdd8e5f73e9",  # noqa
                    }
                },
                "ipython-cosmos-0.1.5/PKG-INFO",
            ],
            "setup.py": [
                "swh:1:cnt:b1e56aad066fcff343882e830cefd0ce082f0ccf",
                {
                    "hashes": {
                        "sha1": "31388c09456c2cb0a741d60c3ca26e5a9b6facbf",
                        "sha256": "51af40f2a7a43c60538d59368671df3f6fb4cd394a7c219bf4c6b20fde4d334c",  # noqa
                    }
                },
                "ipython-cosmos-0.1.5/setup.py",
            ],
            "LICENSE.txt": [
                "swh:1:cnt:05058cca5546507ced02bad620cb7b856ebf5f63",
                {
                    "hashes": {
                        "sha1": "0ec04e5f1e1826931ef4f9446dc0009b41224d1f",
                        "sha256": "55c3b9c2351473c9e61a5b326f631261fd4cb50eec2a7eef750df6ca45150732",  # noqa
                    }
                },
                "ipython-cosmos-0.1.5/LICENSE.txt",
            ],
        },
        # Second response is child details of sub_directory cosmos_sql
        {
            "__init__.py": [
                "swh:1:cnt:aa4046a1143322e93dd86f40861fa0be0b08f07e",
                {
                    "hashes": {
                        "sha1": "978187e0361b2674dbbdd47c824a5e0e5a80c614",
                        "sha256": "9bbe64a2168837d0bbee62f1734077ad3053b6661f8c9b0c9093bdf0224cf183",  # noqa
                    }
                },
                "ipython-cosmos-0.1.5/cosmos_sql/__init__.py",
            ],
            "VERSION": [
                "swh:1:cnt:9faa1b7a7339db85692f91ad4b922554624a3ef7",
                {
                    "hashes": {
                        "sha1": "77ba406cbdaa641f1f4ca09902edf5f03a0e0a1e",
                        "sha256": "800cf1c0392b24de7c0a1c6ea6778ecb433dec71c49a150bce96a98477527b2f",  # noqa
                    }
                },
                "ipython-cosmos-0.1.5/cosmos_sql/VERSION",
            ],
        },
    ]
    test_node = Node(
        name=SAMPLE_ROOT_DIRECTORY_STRUCTURE["name"],
        swhid=SAMPLE_ROOT_DIRECTORY_STRUCTURE["swhid"],
    )
    node_collection = traverse_root(test_node, first_iteration=True)
    expected_node_collection = sample_node_collection
    for item in zip(node_collection.items(), expected_node_collection.items()):
        assert assert_node(item[0][0], item[1][0]) and len(item[0][1]) == len(
            item[1][1]
        )
