from unittest.mock import patch

import pytest

from swh.model.swhids import CoreSWHID, ObjectType
from swh.spdx.node import Node
from swh.spdx.tests.utils import assert_node
from swh.spdx.traverse import traverse_root


@pytest.fixture
def sample_root_directory():
    """
    Represents sample root directory structure
    """
    SAMPLE_ROOT_DIRECTORY_STRUCTURE = {
        "swhid": CoreSWHID(
            object_type=ObjectType.DIRECTORY,
            object_id=bytes.fromhex("7b717af4625b75db3d10709cefcdb620751ec186"),
        ),
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
    return SAMPLE_ROOT_DIRECTORY_STRUCTURE


@pytest.fixture
def sample_node_collection():
    """
    Collection of nodes found in the root directory,
    with keys as root-directory or sub-directories and value as a list of child nodes
    """
    NODE_COLLECTION_OF_SAMPLE_ROOT_DIRECTORY = {
        Node(
            name="ipython-cosmos-0.1.5",
            swhid=CoreSWHID(
                object_type=ObjectType.DIRECTORY,
                object_id=bytes.fromhex("7b717af4625b75db3d10709cefcdb620751ec186"),
            ),  # noqa
            path="ipython-cosmos-0.1.5",
        ): [
            Node(
                name="README.md",
                swhid=CoreSWHID(
                    object_type=ObjectType.CONTENT,
                    object_id=bytes.fromhex("791ff53442a421a68ff9db2e808522adfc4d93ca"),
                ),  # noqa
                path="ipython-cosmos-0.1.5/README.md",
                checksums={
                    "sha1": "5e36830e75ea751e8d1323f4c5bdbfdd0143bdca",
                    "sha256": "7936ae3d6ce0d039223a2fc51c6a6c2ff17e114abf59d0e3e93cc3221dc2161a",  # noqa
                    "sha1_git": "791ff53442a421a68ff9db2e808522adfc4d93ca",
                    "blake2s256": "581a87dedbc3df3174b4a0a11160d0dd5999c4c74c4cfb2803404063b6f25468",  # noqa
                },
            ),
            Node(
                name="cosmos_sql",
                swhid=CoreSWHID(
                    object_type=ObjectType.DIRECTORY,
                    object_id=bytes.fromhex("504251e6894262e5f9c603a7178042e4034dfdc3"),
                ),  # noqa
                path="ipython-cosmos-0.1.5/cosmos_sql",
                checksums={
                    "sha1": "504251e6894262e5f9c603a7178042e4034dfdc3",
                },
            ),
            Node(
                name="PKG-INFO",
                swhid=CoreSWHID(
                    object_type=ObjectType.CONTENT,
                    object_id=bytes.fromhex("bce1e1f42d45a425b828abf2e3b7c45cda6188ca"),
                ),  # noqa
                path="ipython-cosmos-0.1.5/PKG-INFO",
                checksums={
                    "sha1": "b1d809a97e3139f9a9d2890551e5dd448b541202",
                    "sha256": "4a15bc736fbf8a7f9cdeb7b74038d7e033ed0990690c4fc609406cdd8e5f73e9",  # noqa
                    "sha1_git": "bce1e1f42d45a425b828abf2e3b7c45cda6188ca",
                    "blake2s256": "71c8fb6adb5ab28dc814ed67ab2c62a6e20e859081192e18104fd3526a4f658c",  # noqa
                },
            ),
            Node(
                name="setup.py",
                swhid=CoreSWHID(
                    object_type=ObjectType.CONTENT,
                    object_id=bytes.fromhex("b1e56aad066fcff343882e830cefd0ce082f0ccf"),
                ),  # noqa
                path="ipython-cosmos-0.1.5/setup.py",
                checksums={
                    "sha1": "31388c09456c2cb0a741d60c3ca26e5a9b6facbf",
                    "sha256": "51af40f2a7a43c60538d59368671df3f6fb4cd394a7c219bf4c6b20fde4d334c",  # noqa
                    "sha1_git": "b1e56aad066fcff343882e830cefd0ce082f0ccf",
                    "blake2s256": "7212c32f610921a707bfa41f95f414143acd14b8dae2c7ea10fea94dc72efcd5",  # noqa
                },
            ),
            Node(
                name="LICENSE.txt",
                swhid=CoreSWHID(
                    object_type=ObjectType.CONTENT,
                    object_id=bytes.fromhex("05058cca5546507ced02bad620cb7b856ebf5f63"),
                ),  # noqa
                path="ipython-cosmos-0.1.5/LICENSE.txt",
                checksums={
                    "sha1": "0ec04e5f1e1826931ef4f9446dc0009b41224d1f",
                    "sha256": "55c3b9c2351473c9e61a5b326f631261fd4cb50eec2a7eef750df6ca45150732",  # noqa
                    "sha1_git": "05058cca5546507ced02bad620cb7b856ebf5f63",
                    "blake2s256": "1c6311aa1617ba96097942f00facb23549d52cae37ca5914ae3a39b66c2fcd98",  # noqa
                },
            ),
        ],
        Node(
            name="cosmos_sql",
            swhid=CoreSWHID(
                object_type=ObjectType.DIRECTORY,
                object_id=bytes.fromhex("504251e6894262e5f9c603a7178042e4034dfdc3"),
            ),  # noqa
            path="ipython-cosmos-0.1.5/cosmos_sql",
            checksums={
                "sha1": "504251e6894262e5f9c603a7178042e4034dfdc3",
            },
        ): [
            Node(
                name="__init__.py",
                swhid=CoreSWHID(
                    object_type=ObjectType.CONTENT,
                    object_id=bytes.fromhex("aa4046a1143322e93dd86f40861fa0be0b08f07e"),
                ),  # noqa
                path="ipython-cosmos-0.1.5/cosmos_sql/__init__.py",
                checksums={
                    "sha1": "978187e0361b2674dbbdd47c824a5e0e5a80c614",
                    "sha256": "9bbe64a2168837d0bbee62f1734077ad3053b6661f8c9b0c9093bdf0224cf183",  # noqa
                    "sha1_git": "aa4046a1143322e93dd86f40861fa0be0b08f07e",
                    "blake2s256": "45a3fd54b00f0ec1e21431a9ffdcc37dc65045c45c0d3b87443c05ef28a819a5",  # noqa
                },
            ),
            Node(
                name="VERSION",
                swhid=CoreSWHID(
                    object_type=ObjectType.CONTENT,
                    object_id=bytes.fromhex("9faa1b7a7339db85692f91ad4b922554624a3ef7"),
                ),  # noqa
                path="ipython-cosmos-0.1.5/cosmos_sql/VERSION",
                checksums={
                    "sha1": "77ba406cbdaa641f1f4ca09902edf5f03a0e0a1e",
                    "sha256": "800cf1c0392b24de7c0a1c6ea6778ecb433dec71c49a150bce96a98477527b2f",  # noqa
                    "sha1_git": "9faa1b7a7339db85692f91ad4b922554624a3ef7",
                    "blake2s256": "7019ef797a410438ad447fa847b69f90768d909b17aaa70040123e8d7682ff53",  # noqa
                },
            ),
        ],
    }
    return NODE_COLLECTION_OF_SAMPLE_ROOT_DIRECTORY


@patch("swh.spdx.node.get_child")
def test_traverse_root_success(
    mock_get_child, sample_node_collection: dict, sample_root_directory: dict
):
    """
    Tests the traverse_root function over the sample root directory
    """
    mock_get_child.side_effect = [
        # First response is child details of sample_root_directory
        {
            "README.md": [
                CoreSWHID(
                    object_type=ObjectType.CONTENT,
                    object_id=bytes.fromhex("791ff53442a421a68ff9db2e808522adfc4d93ca"),
                ),  # noqa
                {
                    "hashes": {
                        "sha1": "5e36830e75ea751e8d1323f4c5bdbfdd0143bdca",
                        "sha256": "7936ae3d6ce0d039223a2fc51c6a6c2ff17e114abf59d0e3e93cc3221dc2161a",  # noqa
                    }
                },
                "ipython-cosmos-0.1.5/README.md",
            ],
            "cosmos_sql": [
                CoreSWHID(
                    object_type=ObjectType.DIRECTORY,
                    object_id=bytes.fromhex("504251e6894262e5f9c603a7178042e4034dfdc3"),
                ),  # noqa
                {"id": "504251e6894262e5f9c603a7178042e4034dfdc3"},
                "ipython-cosmos-0.1.5/cosmos_sql",
            ],
            "PKG-INFO": [
                CoreSWHID(
                    object_type=ObjectType.CONTENT,
                    object_id=bytes.fromhex("bce1e1f42d45a425b828abf2e3b7c45cda6188ca"),
                ),  # noqa
                {
                    "hashes": {
                        "sha1": "b1d809a97e3139f9a9d2890551e5dd448b541202",
                        "sha256": "4a15bc736fbf8a7f9cdeb7b74038d7e033ed0990690c4fc609406cdd8e5f73e9",  # noqa
                    }
                },
                "ipython-cosmos-0.1.5/PKG-INFO",
            ],
            "setup.py": [
                CoreSWHID(
                    object_type=ObjectType.CONTENT,
                    object_id=bytes.fromhex("b1e56aad066fcff343882e830cefd0ce082f0ccf"),
                ),  # noqa
                {
                    "hashes": {
                        "sha1": "31388c09456c2cb0a741d60c3ca26e5a9b6facbf",
                        "sha256": "51af40f2a7a43c60538d59368671df3f6fb4cd394a7c219bf4c6b20fde4d334c",  # noqa
                    }
                },
                "ipython-cosmos-0.1.5/setup.py",
            ],
            "LICENSE.txt": [
                CoreSWHID(
                    object_type=ObjectType.CONTENT,
                    object_id=bytes.fromhex("05058cca5546507ced02bad620cb7b856ebf5f63"),
                ),  # noqa
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
                CoreSWHID(
                    object_type=ObjectType.CONTENT,
                    object_id=bytes.fromhex("aa4046a1143322e93dd86f40861fa0be0b08f07e"),
                ),  # noqa
                {
                    "hashes": {
                        "sha1": "978187e0361b2674dbbdd47c824a5e0e5a80c614",
                        "sha256": "9bbe64a2168837d0bbee62f1734077ad3053b6661f8c9b0c9093bdf0224cf183",  # noqa
                    }
                },
                "ipython-cosmos-0.1.5/cosmos_sql/__init__.py",
            ],
            "VERSION": [
                CoreSWHID(
                    object_type=ObjectType.CONTENT,
                    object_id=bytes.fromhex("9faa1b7a7339db85692f91ad4b922554624a3ef7"),
                ),  # noqa
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
        name=sample_root_directory["name"],
        swhid=sample_root_directory["swhid"],
    )
    node_collection = traverse_root(test_node, first_iteration=True)
    expected_node_collection = sample_node_collection
    for item in zip(node_collection.items(), expected_node_collection.items()):
        assert assert_node(item[0][0], item[1][0]) and len(item[0][1]) == len(
            item[1][1]
        )
