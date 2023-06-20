import unittest
from unittest.mock import patch

from swh.spdx.children import get_child


class TestGetChild(unittest.TestCase):
    @patch("gql.Client.execute")
    def test_get_child_data_success_without_cursor(self, mock_get):
        """
        Test case for retrieving child data successfully without a cursor.
        """
        mock_response = {
            "directory": {
                "swhid": "swh:1:dir:f2950cf58e4cbff02bbbfa648c1867067116b06b",
                "entries": {
                    "totalCount": 3,
                    "pageInfo": {"endCursor": None},
                    "edges": [
                        {
                            "node": {
                                "name": {"text": "icon.py"},
                                "target": {
                                    "swhid": "swh:1:cnt:5a8ab8a8b9a5c2ecfceb6027ae5ebe4893e131cb",  # noqa
                                    "node": {
                                        "hashes": {
                                            "sha1": "91892edeaec16566b2b1c6d75aa5b9436bebc102",  # noqa
                                            "sha256": "20f503784af711179c1b47d5253ecef86c5b09a2cfd2e74c6df2e8e4c180f3e9",  # noqa
                                        }
                                    },
                                },
                            }
                        },
                        {
                            "node": {
                                "name": {"text": "syntax_helpers.py"},
                                "target": {
                                    "swhid": "swh:1:cnt:7994a69e5ec1582f8f8807e31384ba399ba64d13",  # noqa
                                    "node": {
                                        "hashes": {
                                            "sha1": "48d059e0697cc6bd6c7bc5c5a459f1d55510b872",  # noqa
                                            "sha256": "252a6a02cdce7889737d9926f736a561f5615170fd5dc0ee67fe89e496b1a810",  # noqa
                                        }
                                    },
                                },
                            }
                        },
                        {
                            "node": {
                                "name": {"text": "__init__.py"},
                                "target": {
                                    "swhid": "swh:1:cnt:eb458961d5b0dba8c463c5e2566e03dc7b24b18a",  # noqa
                                    "node": {
                                        "hashes": {
                                            "sha1": "fa0e3a31934c51ed0acae2f4957f921794a8b5ff",  # noqa
                                            "sha256": "a37e861d22df4103fa4abbfc488affbe3b815f3933174f210110e83d2d2b0d1a",  # noqa
                                        }
                                    },
                                },
                            }
                        },
                    ],
                },
            }
        }
        mock_get.return_value = mock_response

        result = get_child("swh:1:dir:f2950cf58e4cbff02bbbfa648c1867067116b06b")
        expected_result = {
            "icon.py": [
                "swh:1:cnt:5a8ab8a8b9a5c2ecfceb6027ae5ebe4893e131cb",
                {
                    "hashes": {
                        "sha1": "91892edeaec16566b2b1c6d75aa5b9436bebc102",
                        "sha256": "20f503784af711179c1b47d5253ecef86c5b09a2cfd2e74c6df2e8e4c180f3e9",  # noqa
                    }
                },
            ],
            "syntax_helpers.py": [
                "swh:1:cnt:7994a69e5ec1582f8f8807e31384ba399ba64d13",
                {
                    "hashes": {
                        "sha1": "48d059e0697cc6bd6c7bc5c5a459f1d55510b872",
                        "sha256": "252a6a02cdce7889737d9926f736a561f5615170fd5dc0ee67fe89e496b1a810",  # noqa
                    }
                },
            ],
            "__init__.py": [
                "swh:1:cnt:eb458961d5b0dba8c463c5e2566e03dc7b24b18a",
                {
                    "hashes": {
                        "sha1": "fa0e3a31934c51ed0acae2f4957f921794a8b5ff",
                        "sha256": "a37e861d22df4103fa4abbfc488affbe3b815f3933174f210110e83d2d2b0d1a",  # noqa
                    }
                },
            ],
        }

        self.assertEqual(result, expected_result)

    @patch("gql.Client.execute")
    def test_get_child_data_success_with_cursor(self, mock_get):
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
                        "pageInfo": {"endCursor": "MTI="},
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
                        "pageInfo": {"endCursor": None},
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

        result = get_child("swh:1:dir:d4c2954acfd72686a1b80e6217ddd2d7a9f09324")

        expected_result = {
            "README.md": [
                "swh:1:cnt:d64a256e7816aa1c8bcda766597b3ae8dca0eabc",
                {
                    "hashes": {
                        "sha1": "08b0b931d7d7566b7d88b712ff38e04e129331ad",
                        "sha256": "3af77bd23c20924fcd0b2b5fcefd60d4c27a35f27c88de9bf5a9d69205afe083",  # noqa
                    }
                },
            ],
            "LICENSE": [
                "swh:1:cnt:cf5c9507a06465fb3150db73edb36d9509e0aa27",
                {
                    "hashes": {
                        "sha1": "3881eb883085c17fe3e91a68dd3e9699b47451bd",
                        "sha256": "82d969ac679a3da7ca44fec2d9b3b1d80de6e89186a32975c061a6a9bdde6d01",  # noqa
                    }
                },
            ],
            "index.rst": [
                "swh:1:cnt:21f09f999e058cfdfc65882dcb86c5e97ed751ae",
                {
                    "hashes": {
                        "sha1": "326614be19d806e966d41de540e02a5eb5abf90f",
                        "sha256": "c47a4e071f9be95800d12f362eeaa92361f65d0a33ab186749fc2484fcef203e",  # noqa
                    }
                },
            ],
            "Makefile": [
                "swh:1:cnt:c447ddd50823a13330ac2fa2781058b08fe65d94",
                {
                    "hashes": {
                        "sha1": "a490b7783ef92495c556283ad757bca582c5ee55",
                        "sha256": "d4fc8a80271f9eecf393d77f202515da5af5d19892269c9d6e68e56c47fcf76c",  # noqa
                    }
                },
            ],
            "setup.py": [
                "swh:1:cnt:d285c4028b8fc66f459fd5c7a4394df79a399882",
                {
                    "hashes": {
                        "sha1": "0dc4142c4b312421aca5ccfdbcd3edbb3b886a96",
                        "sha256": "10bfeef758005c77b9bdecf553b90430ee7cc6fd3e4578d32093d602249168c9",  # noqa
                    }
                },
            ],
            "logtree": [
                "swh:1:dir:d7f188b69f207b498f8acd8d20dff39f8c3611e6",
                {"id": "d7f188b69f207b498f8acd8d20dff39f8c3611e6"},
            ],
            "pyproject.toml": [
                "swh:1:cnt:665bffe1294c39c223dd6d185d79ebca8c5558fe",
                {
                    "hashes": {
                        "sha1": "b3cbc59fade196ab914f7c7777fb199127e29c7f",
                        "sha256": "e4ac64a2ce0cfc15a9711ed3efa28c38598f2a6ff160f1b5fcca5808be6a36ff",  # noqa
                    }
                },
            ],
            "PKG-INFO": [
                "swh:1:cnt:f9fb843aa9373b614b4625a5e5c15241c40ee9ad",
                {
                    "hashes": {
                        "sha1": "fe6c9530e627e2af17deb1bf9e17d89735a4401f",
                        "sha256": "42a644a672fa9d1b85efa90d892a03b0511a27480396fb35bbbe3098ab8707dd",  # noqa
                    }
                },
            ],
            "conf.py": [
                "swh:1:cnt:5168b27b29e58f437e55fe0c5e624317a077b313",
                {
                    "hashes": {
                        "sha1": "da2cc86a9ca2683e0326320622a7e71ab365712c",
                        "sha256": "671507ebf18ae77dd3f5d8b1fc02c9d693f659531e0131ef8174090a00fc50d5",  # noqa
                    }
                },
            ],
            ".gitignore": [
                "swh:1:cnt:9491b08aad2f7ae39bc1317b8474c44b3f84c6ec",
                {
                    "hashes": {
                        "sha1": "e8750e13f5a0c71fb48975a07d844b63634b0ed3",
                        "sha256": "6441634f36913f40b67ff82bb0c943846d224e991224f1679c2a6a992ba881fc",  # noqa
                    }
                },
            ],
            "shell.nix": [
                "swh:1:cnt:381a6e360d59224ca87d5bd210819a1e93864a35",
                {
                    "hashes": {
                        "sha1": "af790abb41f0e674633fa5e8bd0ffb9383da99ae",
                        "sha256": "27c99c91835cf2aced89130c4c9e2219cabba5a42d31b8acc64d46fd9073968c",  # noqa
                    }
                },
            ],
            "release": [
                "swh:1:cnt:e81b9f61ed0a45313d1a9063a44481d13fbd7840",
                {
                    "hashes": {
                        "sha1": "e5ae14d62f0b6c09c8ab2e1f5f480ab72cdc8de0",
                        "sha256": "b8c918feaa5e8b0acc966b54b8663be342abc6de094738e5be7d91f4149077f9",  # noqa
                    }
                },
            ],
            "test.py": [
                "swh:1:cnt:cfd24586131109bb28e43ff71fa71a7099bf7e0a",
                {
                    "hashes": {
                        "sha1": "b00b129a06de13b127a227dacc0c4cfa1f10829d",
                        "sha256": "5ee65b9c98a9b6afce1a95b7629f0a18cfbfce84b927fb3d5cbd563fe66a6b2d",  # noqa
                    }
                },
            ],
        }

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
