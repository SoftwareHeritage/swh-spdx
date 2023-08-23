import requests
from requests.exceptions import HTTPError

from swh.spdx.connection import get_graphql_client
from swh.spdx.query import get_query_content


def get_content_from_hashes(content_object_checksums: dict) -> str:
    client = get_graphql_client()
    query = get_query_content()
    params = {
        "sha1": content_object_checksums["sha1"],
        "sha256": content_object_checksums["sha256"],
        "sha1_git": content_object_checksums["sha1_git"],
        "blake2s256": content_object_checksums["blake2s256"],
    }
    response = client.execute(query, params)
    raw_content = response["contentByHashes"]["data"]["raw"]
    if raw_content is None:
        # Content size exceeded 10000 bytes
        content_download_url = response["contentByHashes"]["data"]["url"]
        downloaded_content = requests.get(content_download_url)
        if not downloaded_content.status_code == 200:
            raise HTTPError("Error downloading content")
        return downloaded_content.text
    text_content = raw_content["text"]
    return text_content
