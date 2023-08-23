from unittest.mock import patch

import pytest

from swh.spdx.content import get_content_from_hashes


@pytest.fixture
def empty_content_object_hashes():
    # Not actually empty but contains a empty line - "\n"
    hashes = {
        "sha1": "adc83b19e793491b1c6ea0fd8b46cd9f32e592fc",
        "sha256": "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b",
        "sha1_git": "8b137891791fe96927ad78e64b0aad7bded08bdc",
        "blake2s256": "6fa16ac015c6513f6b98ee9e3f771ca8324a0ce77fbb9337fe3f8f549643dc73",
    }
    return hashes


@pytest.fixture
def non_empty_content_object_hashes():
    # Has content "a_cv2_text_effects\n"
    hashes = {
        "sha1": "b6b52b421d2b70dc9091fcee8c4d64f151eb3690",
        "sha256": "7071a2aeb4d76a314773e5085094ad771ab0d56d3a50313715a9f15269418544",
        "sha1_git": "eba78c7438d05474605f79d0a68affbf805e2309",
        "blake2s256": "7992173ca53c1d6d0da20d03cc79067b3832525e31352dcd2f18ac842659c38a",
    }
    return hashes


@patch("gql.Client.execute")
def test_empty_content(mock, empty_content_object_hashes: dict):
    """
    Tests the get_content_from_hashes() on empty content object
    """
    mock.return_value = {
        "contentByHashes": {
            "data": {
                "url": "https://archive.softwareheritage.org/api/1/content/sha1:adc83b19e793491b1c6ea0fd8b46cd9f32e592fc/raw/",  # noqa
                "raw": {"text": "\n"},
            }
        }
    }
    text_content = get_content_from_hashes(empty_content_object_hashes)
    assert text_content == "\n"


@patch("gql.Client.execute")
def test_non_empty_content(mock, non_empty_content_object_hashes: dict):
    """
    Tests the get_content_from_hashes() on non-empty content object
    """
    mock.return_value = {
        "contentByHashes": {
            "data": {
                "url": "https://archive.softwareheritage.org/api/1/content/sha1:b6b52b421d2b70dc9091fcee8c4d64f151eb3690/raw/",  # noqa
                "raw": {"text": "a_cv2_text_effects\n"},
            }
        }
    }
    text_content = get_content_from_hashes(non_empty_content_object_hashes)
    assert text_content == "a_cv2_text_effects\n"
