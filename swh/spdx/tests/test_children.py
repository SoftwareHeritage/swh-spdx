from unittest.mock import patch

import pytest

from swh.model.swhids import CoreSWHID, ObjectType
from swh.spdx.children import get_child


@patch("gql.Client.execute")
def test_get_child_data_success(mock_get):
    """
    Test case for retrieving child data successfully with a cursor.
    """
    mock_get.side_effect = [
        # First mock_response with cursor
        {
            "directory": {
                "swhid": "swh:1:dir:d4c2954acfd72686a1b80e6217ddd2d7a9f09324",
                "entries": {
                    "totalCount": 13,
                    "pageInfo": {
                        "endCursor": "MTI=",
                        "hasNextPage": True,
                    },
                    "edges": [
                        {
                            "node": {
                                "name": {"text": "README.md"},
                                "target": {
                                    "swhid": "swh:1:cnt:d64a256e7816aa1c8bcda766597b3ae8dca0eabc",  # noqa
                                    "node": {
                                        "hashes": {
                                            "sha1": "08b0b931d7d7566b7d88b712ff38e04e129331ad",  # noqa
                                            "sha256": "3af77bd23c20924fcd0b2b5fcefd60d4c27a35f27c88de9bf5a9d69205afe083",  # noqa
                                            "sha1_git": "d64a256e7816aa1c8bcda766597b3ae8dca0eabc",  # noqa
                                            "blake2s256": "0affbded2ce35080e559a3012c56f3a60833754bf96b7bad691c8e824e2a3853",  # noqa
                                        }
                                    },
                                },
                            }
                        },
                        {
                            "node": {
                                "name": {"text": "LICENSE"},
                                "target": {
                                    "swhid": "swh:1:cnt:cf5c9507a06465fb3150db73edb36d9509e0aa27",  # noqa
                                    "node": {
                                        "hashes": {
                                            "sha1": "3881eb883085c17fe3e91a68dd3e9699b47451bd",  # noqa
                                            "sha256": "82d969ac679a3da7ca44fec2d9b3b1d80de6e89186a32975c061a6a9bdde6d01",  # noqa
                                            "sha1_git": "cf5c9507a06465fb3150db73edb36d9509e0aa27",  # noqa
                                            "blake2s256": "ce855d433513f1dcb078658177362468e063360c11ded0d059e5675926410a7f",  # noqa
                                        }
                                    },
                                },
                            }
                        },
                        {
                            "node": {
                                "name": {"text": "index.rst"},
                                "target": {
                                    "swhid": "swh:1:cnt:21f09f999e058cfdfc65882dcb86c5e97ed751ae",  # noqa
                                    "node": {
                                        "hashes": {
                                            "sha1": "326614be19d806e966d41de540e02a5eb5abf90f",  # noqa
                                            "sha256": "c47a4e071f9be95800d12f362eeaa92361f65d0a33ab186749fc2484fcef203e",  # noqa
                                            "sha1_git": "21f09f999e058cfdfc65882dcb86c5e97ed751ae",  # noqa
                                            "blake2s256": "1cf9b521337bf22762a0e37343c6dedb8edec73aea517275c4d9c34047e0854b",  # noqa
                                        }
                                    },
                                },
                            }
                        },
                        {
                            "node": {
                                "name": {"text": "Makefile"},
                                "target": {
                                    "swhid": "swh:1:cnt:c447ddd50823a13330ac2fa2781058b08fe65d94",  # noqa
                                    "node": {
                                        "hashes": {
                                            "sha1": "a490b7783ef92495c556283ad757bca582c5ee55",  # noqa
                                            "sha256": "d4fc8a80271f9eecf393d77f202515da5af5d19892269c9d6e68e56c47fcf76c",  # noqa
                                            "sha1_git": "c447ddd50823a13330ac2fa2781058b08fe65d94",  # noqa
                                            "blake2s256": "8d5fd66394971023fd09106b3b9e02cfe0ffe23b061bf12d491a8f8ac99bb44b",  # noqa
                                        }
                                    },
                                },
                            }
                        },
                        {
                            "node": {
                                "name": {"text": "setup.py"},
                                "target": {
                                    "swhid": "swh:1:cnt:d285c4028b8fc66f459fd5c7a4394df79a399882",  # noqa
                                    "node": {
                                        "hashes": {
                                            "sha1": "0dc4142c4b312421aca5ccfdbcd3edbb3b886a96",  # noqa
                                            "sha256": "10bfeef758005c77b9bdecf553b90430ee7cc6fd3e4578d32093d602249168c9",  # noqa
                                            "sha1_git": "d285c4028b8fc66f459fd5c7a4394df79a399882",  # noqa
                                            "blake2s256": "268d2d07217c7600a5dbb1d2159d1d12d0bd275683e31c238e8e499c0e86738e",  # noqa
                                        }
                                    },
                                },
                            }
                        },
                        {
                            "node": {
                                "name": {"text": "logtree"},
                                "target": {
                                    "swhid": "swh:1:dir:d7f188b69f207b498f8acd8d20dff39f8c3611e6",  # noqa
                                    "node": {
                                        "id": "d7f188b69f207b498f8acd8d20dff39f8c3611e6"
                                    },
                                },
                            }
                        },
                        {
                            "node": {
                                "name": {"text": "pyproject.toml"},
                                "target": {
                                    "swhid": "swh:1:cnt:665bffe1294c39c223dd6d185d79ebca8c5558fe",  # noqa
                                    "node": {
                                        "hashes": {
                                            "sha1": "b3cbc59fade196ab914f7c7777fb199127e29c7f",  # noqa
                                            "sha256": "e4ac64a2ce0cfc15a9711ed3efa28c38598f2a6ff160f1b5fcca5808be6a36ff",  # noqa
                                            "sha1_git": "665bffe1294c39c223dd6d185d79ebca8c5558fe",  # noqa
                                            "blake2s256": "37f4b30a9f576494d087c9916984a5e8249fb0aeaebaedac83424774a64a282e",  # noqa
                                        }
                                    },
                                },
                            }
                        },
                        {
                            "node": {
                                "name": {"text": "PKG-INFO"},
                                "target": {
                                    "swhid": "swh:1:cnt:f9fb843aa9373b614b4625a5e5c15241c40ee9ad",  # noqa
                                    "node": {
                                        "hashes": {
                                            "sha1": "fe6c9530e627e2af17deb1bf9e17d89735a4401f",  # noqa
                                            "sha256": "42a644a672fa9d1b85efa90d892a03b0511a27480396fb35bbbe3098ab8707dd",  # noqa
                                            "sha1_git": "f9fb843aa9373b614b4625a5e5c15241c40ee9ad",  # noqa
                                            "blake2s256": "4a88b45f14fceca57570a6b57ceeff2ae385bbf54954f8e0790ff68b9afab456",  # noqa
                                        }
                                    },
                                },
                            }
                        },
                        {
                            "node": {
                                "name": {"text": "conf.py"},
                                "target": {
                                    "swhid": "swh:1:cnt:5168b27b29e58f437e55fe0c5e624317a077b313",  # noqa
                                    "node": {
                                        "hashes": {
                                            "sha1": "da2cc86a9ca2683e0326320622a7e71ab365712c",  # noqa
                                            "sha256": "671507ebf18ae77dd3f5d8b1fc02c9d693f659531e0131ef8174090a00fc50d5",  # noqa
                                            "sha1_git": "5168b27b29e58f437e55fe0c5e624317a077b313",  # noqa
                                            "blake2s256": "8968cba82cd85736de3c56cc24512513f10bb352514267367365bdf9ce925d5d",  # noqa
                                        }
                                    },
                                },
                            }
                        },
                        {
                            "node": {
                                "name": {"text": ".gitignore"},
                                "target": {
                                    "swhid": "swh:1:cnt:9491b08aad2f7ae39bc1317b8474c44b3f84c6ec",  # noqa
                                    "node": {
                                        "hashes": {
                                            "sha1": "e8750e13f5a0c71fb48975a07d844b63634b0ed3",  # noqa
                                            "sha256": "6441634f36913f40b67ff82bb0c943846d224e991224f1679c2a6a992ba881fc",  # noqa
                                            "sha1_git": "9491b08aad2f7ae39bc1317b8474c44b3f84c6ec",  # noqa
                                            "blake2s256": "e201de69f139ce2875c0e11bf4e7d2548bcae86f543d3db8ace5fe199efdb5f3",  # noqa
                                        }
                                    },
                                },
                            }
                        },
                        {
                            "node": {
                                "name": {"text": "shell.nix"},
                                "target": {
                                    "swhid": "swh:1:cnt:381a6e360d59224ca87d5bd210819a1e93864a35",  # noqa
                                    "node": {
                                        "hashes": {
                                            "sha1": "af790abb41f0e674633fa5e8bd0ffb9383da99ae",  # noqa
                                            "sha256": "27c99c91835cf2aced89130c4c9e2219cabba5a42d31b8acc64d46fd9073968c",  # noqa
                                            "sha1_git": "381a6e360d59224ca87d5bd210819a1e93864a35",  # noqa
                                            "blake2s256": "55e2b81c3192b10cb304fa354c6f60c1ad87cd3e78e6cce1bf3d216e77468c82",  # noqa
                                        }
                                    },
                                },
                            }
                        },
                        {
                            "node": {
                                "name": {"text": "release"},
                                "target": {
                                    "swhid": "swh:1:cnt:e81b9f61ed0a45313d1a9063a44481d13fbd7840",  # noqa
                                    "node": {
                                        "hashes": {
                                            "sha1": "e5ae14d62f0b6c09c8ab2e1f5f480ab72cdc8de0",  # noqa
                                            "sha256": "b8c918feaa5e8b0acc966b54b8663be342abc6de094738e5be7d91f4149077f9",  # noqa
                                            "sha1_git": "e81b9f61ed0a45313d1a9063a44481d13fbd7840",  # noqa
                                            "blake2s256": "b4ec14d6a7cda7475b8d7d4cc23f7751cfb1ffced43a9b80c0d2837e42356725",  # noqa
                                        }
                                    },
                                },
                            }
                        },
                    ],
                },
            }
        },
        # Second mock_response without cursor
        {
            "directory": {
                "swhid": "swh:1:dir:d4c2954acfd72686a1b80e6217ddd2d7a9f09324",
                "entries": {
                    "totalCount": 13,
                    "pageInfo": {
                        "endCursor": None,
                        "hasNextPage": False,
                    },
                    "edges": [
                        {
                            "node": {
                                "name": {"text": "test.py"},
                                "target": {
                                    "swhid": "swh:1:cnt:cfd24586131109bb28e43ff71fa71a7099bf7e0a",  # noqa
                                    "node": {
                                        "hashes": {
                                            "sha1": "b00b129a06de13b127a227dacc0c4cfa1f10829d",  # noqa
                                            "sha256": "5ee65b9c98a9b6afce1a95b7629f0a18cfbfce84b927fb3d5cbd563fe66a6b2d",  # noqa
                                            "sha1_git": "cfd24586131109bb28e43ff71fa71a7099bf7e0a",  # noqa
                                            "blake2s256": "e1739a6dfd22303ac4e9fec2bc944cb812102e58ecd152889a872ebccadbf1eb",  # noqa
                                        }
                                    },
                                },
                            }
                        }
                    ],
                },
            }
        },
    ]

    result = get_child(
        dir_swhid=CoreSWHID(
            object_type=ObjectType.DIRECTORY,
            object_id=bytes.fromhex("d4c2954acfd72686a1b80e6217ddd2d7a9f09324"),
        ),
        dir_name="logtree-1.1",
    )

    expected_result = {
        "README.md": [
            CoreSWHID(
                object_type=ObjectType.CONTENT,
                object_id=bytes.fromhex("d64a256e7816aa1c8bcda766597b3ae8dca0eabc"),
            ),
            {
                "hashes": {
                    "sha1": "08b0b931d7d7566b7d88b712ff38e04e129331ad",
                    "sha256": "3af77bd23c20924fcd0b2b5fcefd60d4c27a35f27c88de9bf5a9d69205afe083",  # noqa
                    "sha1_git": "d64a256e7816aa1c8bcda766597b3ae8dca0eabc",
                    "blake2s256": "0affbded2ce35080e559a3012c56f3a60833754bf96b7bad691c8e824e2a3853",  # noqa
                }
            },
            "logtree-1.1/README.md",
        ],
        "LICENSE": [
            CoreSWHID(
                object_type=ObjectType.CONTENT,
                object_id=bytes.fromhex("cf5c9507a06465fb3150db73edb36d9509e0aa27"),
            ),
            {
                "hashes": {
                    "sha1": "3881eb883085c17fe3e91a68dd3e9699b47451bd",
                    "sha256": "82d969ac679a3da7ca44fec2d9b3b1d80de6e89186a32975c061a6a9bdde6d01",  # noqa
                    "sha1_git": "cf5c9507a06465fb3150db73edb36d9509e0aa27",
                    "blake2s256": "ce855d433513f1dcb078658177362468e063360c11ded0d059e5675926410a7f",  # noqa
                }
            },
            "logtree-1.1/LICENSE",
        ],
        "index.rst": [
            CoreSWHID(
                object_type=ObjectType.CONTENT,
                object_id=bytes.fromhex("21f09f999e058cfdfc65882dcb86c5e97ed751ae"),
            ),
            {
                "hashes": {
                    "sha1": "326614be19d806e966d41de540e02a5eb5abf90f",
                    "sha256": "c47a4e071f9be95800d12f362eeaa92361f65d0a33ab186749fc2484fcef203e",  # noqa
                    "sha1_git": "21f09f999e058cfdfc65882dcb86c5e97ed751ae",
                    "blake2s256": "1cf9b521337bf22762a0e37343c6dedb8edec73aea517275c4d9c34047e0854b",  # noqa
                }
            },
            "logtree-1.1/index.rst",
        ],
        "Makefile": [
            CoreSWHID(
                object_type=ObjectType.CONTENT,
                object_id=bytes.fromhex("c447ddd50823a13330ac2fa2781058b08fe65d94"),
            ),
            {
                "hashes": {
                    "sha1": "a490b7783ef92495c556283ad757bca582c5ee55",
                    "sha256": "d4fc8a80271f9eecf393d77f202515da5af5d19892269c9d6e68e56c47fcf76c",  # noqa
                    "sha1_git": "c447ddd50823a13330ac2fa2781058b08fe65d94",
                    "blake2s256": "8d5fd66394971023fd09106b3b9e02cfe0ffe23b061bf12d491a8f8ac99bb44b",  # noqa
                }
            },
            "logtree-1.1/Makefile",
        ],
        "setup.py": [
            CoreSWHID(
                object_type=ObjectType.CONTENT,
                object_id=bytes.fromhex("d285c4028b8fc66f459fd5c7a4394df79a399882"),
            ),
            {
                "hashes": {
                    "sha1": "0dc4142c4b312421aca5ccfdbcd3edbb3b886a96",
                    "sha256": "10bfeef758005c77b9bdecf553b90430ee7cc6fd3e4578d32093d602249168c9",  # noqa
                    "sha1_git": "d285c4028b8fc66f459fd5c7a4394df79a399882",
                    "blake2s256": "268d2d07217c7600a5dbb1d2159d1d12d0bd275683e31c238e8e499c0e86738e",  # noqa
                }
            },
            "logtree-1.1/setup.py",
        ],
        "logtree": [
            CoreSWHID(
                object_type=ObjectType.DIRECTORY,
                object_id=bytes.fromhex("d7f188b69f207b498f8acd8d20dff39f8c3611e6"),
            ),
            {"id": "d7f188b69f207b498f8acd8d20dff39f8c3611e6"},
            "logtree-1.1/logtree",
        ],
        "pyproject.toml": [
            CoreSWHID(
                object_type=ObjectType.CONTENT,
                object_id=bytes.fromhex("665bffe1294c39c223dd6d185d79ebca8c5558fe"),
            ),
            {
                "hashes": {
                    "sha1": "b3cbc59fade196ab914f7c7777fb199127e29c7f",
                    "sha256": "e4ac64a2ce0cfc15a9711ed3efa28c38598f2a6ff160f1b5fcca5808be6a36ff",  # noqa
                    "sha1_git": "665bffe1294c39c223dd6d185d79ebca8c5558fe",
                    "blake2s256": "37f4b30a9f576494d087c9916984a5e8249fb0aeaebaedac83424774a64a282e",  # noqa
                }
            },
            "logtree-1.1/pyproject.toml",
        ],
        "PKG-INFO": [
            CoreSWHID(
                object_type=ObjectType.CONTENT,
                object_id=bytes.fromhex("f9fb843aa9373b614b4625a5e5c15241c40ee9ad"),
            ),
            {
                "hashes": {
                    "sha1": "fe6c9530e627e2af17deb1bf9e17d89735a4401f",
                    "sha256": "42a644a672fa9d1b85efa90d892a03b0511a27480396fb35bbbe3098ab8707dd",  # noqa
                    "sha1_git": "f9fb843aa9373b614b4625a5e5c15241c40ee9ad",
                    "blake2s256": "4a88b45f14fceca57570a6b57ceeff2ae385bbf54954f8e0790ff68b9afab456",  # noqa
                }
            },
            "logtree-1.1/PKG-INFO",
        ],
        "conf.py": [
            CoreSWHID(
                object_type=ObjectType.CONTENT,
                object_id=bytes.fromhex("5168b27b29e58f437e55fe0c5e624317a077b313"),
            ),
            {
                "hashes": {
                    "sha1": "da2cc86a9ca2683e0326320622a7e71ab365712c",
                    "sha256": "671507ebf18ae77dd3f5d8b1fc02c9d693f659531e0131ef8174090a00fc50d5",  # noqa
                    "sha1_git": "5168b27b29e58f437e55fe0c5e624317a077b313",
                    "blake2s256": "8968cba82cd85736de3c56cc24512513f10bb352514267367365bdf9ce925d5d",  # noqa
                }
            },
            "logtree-1.1/conf.py",
        ],
        ".gitignore": [
            CoreSWHID(
                object_type=ObjectType.CONTENT,
                object_id=bytes.fromhex("9491b08aad2f7ae39bc1317b8474c44b3f84c6ec"),
            ),
            {
                "hashes": {
                    "sha1": "e8750e13f5a0c71fb48975a07d844b63634b0ed3",
                    "sha256": "6441634f36913f40b67ff82bb0c943846d224e991224f1679c2a6a992ba881fc",  # noqa
                    "sha1_git": "9491b08aad2f7ae39bc1317b8474c44b3f84c6ec",
                    "blake2s256": "e201de69f139ce2875c0e11bf4e7d2548bcae86f543d3db8ace5fe199efdb5f3",  # noqa
                }
            },
            "logtree-1.1/.gitignore",
        ],
        "shell.nix": [
            CoreSWHID(
                object_type=ObjectType.CONTENT,
                object_id=bytes.fromhex("381a6e360d59224ca87d5bd210819a1e93864a35"),
            ),
            {
                "hashes": {
                    "sha1": "af790abb41f0e674633fa5e8bd0ffb9383da99ae",
                    "sha256": "27c99c91835cf2aced89130c4c9e2219cabba5a42d31b8acc64d46fd9073968c",  # noqa
                    "sha1_git": "381a6e360d59224ca87d5bd210819a1e93864a35",
                    "blake2s256": "55e2b81c3192b10cb304fa354c6f60c1ad87cd3e78e6cce1bf3d216e77468c82",  # noqa
                }
            },
            "logtree-1.1/shell.nix",
        ],
        "release": [
            CoreSWHID(
                object_type=ObjectType.CONTENT,
                object_id=bytes.fromhex("e81b9f61ed0a45313d1a9063a44481d13fbd7840"),
            ),
            {
                "hashes": {
                    "sha1": "e5ae14d62f0b6c09c8ab2e1f5f480ab72cdc8de0",
                    "sha256": "b8c918feaa5e8b0acc966b54b8663be342abc6de094738e5be7d91f4149077f9",  # noqa
                    "sha1_git": "e81b9f61ed0a45313d1a9063a44481d13fbd7840",
                    "blake2s256": "b4ec14d6a7cda7475b8d7d4cc23f7751cfb1ffced43a9b80c0d2837e42356725",  # noqa
                }
            },
            "logtree-1.1/release",
        ],
        "test.py": [
            CoreSWHID(
                object_type=ObjectType.CONTENT,
                object_id=bytes.fromhex("cfd24586131109bb28e43ff71fa71a7099bf7e0a"),
            ),
            {
                "hashes": {
                    "sha1": "b00b129a06de13b127a227dacc0c4cfa1f10829d",
                    "sha256": "5ee65b9c98a9b6afce1a95b7629f0a18cfbfce84b927fb3d5cbd563fe66a6b2d",  # noqa
                    "sha1_git": "cfd24586131109bb28e43ff71fa71a7099bf7e0a",
                    "blake2s256": "e1739a6dfd22303ac4e9fec2bc944cb812102e58ecd152889a872ebccadbf1eb",  # noqa
                }
            },
            "logtree-1.1/test.py",
        ],
    }

    assert result == expected_result


@pytest.mark.parametrize(
    "invalid_dir_swhid, expected_exception",
    [
        (
            CoreSWHID(
                object_type=ObjectType.CONTENT,
                object_id=bytes.fromhex("6e73f50e8f1176fe1b5907ce973f14381008fa79"),
            ),
            ValueError,
        ),
        (
            CoreSWHID(
                object_type=ObjectType.REVISION,
                object_id=bytes.fromhex("6dd0504b43b4459d52e9f13f71a91cc0fc445a19"),
            ),
            ValueError,
        ),
        (
            CoreSWHID(
                object_type=ObjectType.SNAPSHOT,
                object_id=bytes.fromhex("6436d2c9b06cf9bd9efb0b4e463c3fe6b868eadc"),
            ),
            ValueError,
        ),
    ],
)
def test_get_child_invalid_swhid(
    invalid_dir_swhid: CoreSWHID, expected_exception: Exception
):
    """
    test case for checking exception handling
    when parametrizing core swhids other than directory swhids
    """
    with pytest.raises(ValueError):
        get_child(
            invalid_dir_swhid,
            "test_string",  # to invoke the exception used "test_string" as dir_name argument
        )
