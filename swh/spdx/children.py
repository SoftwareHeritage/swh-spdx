from swh.model.swhids import CoreSWHID, ObjectType
from swh.spdx.connection import get_graphql_client
from swh.spdx.query import get_query_children


def get_child(dir_swhid: CoreSWHID, dir_name: str) -> dict:
    """
    Retrieves the child details of a directory specified by its SWHID.

    Args:
        dir_swhid (CoreSWHID): The SWHID of the directory.
        dir_name (str): The name of the directory whose children details needs to be retrieved.

    Returns:
        Dict[str: List]: A dictionary containing the child details,
        where the keys are child names and the values is a list of swhid,
        checksums and directory path of child.
    """
    if not dir_swhid.object_type == ObjectType.DIRECTORY:
        raise ValueError(f"{str(dir_swhid)} is not a valid directory SWHID")
    client = get_graphql_client()
    has_next_page = True
    cursor = None
    # Initialize child details as empty dictionary
    child_details = {}
    query = get_query_children()
    while has_next_page:
        params = {"swhid": str(dir_swhid), "cursor": cursor}
        response = client.execute(query, params)
        page_info = response["directory"]["entries"]["pageInfo"]
        has_next_page = page_info["hasNextPage"]
        cursor = page_info["endCursor"]
        edges = response["directory"]["entries"]["edges"]
        for edge in edges:
            node = edge["node"]
            child_name = node["name"]["text"]
            child_path = f"{dir_name}/{child_name}"
            str_child_swhid = node["target"]["swhid"]
            child_swhid = CoreSWHID.from_string(str_child_swhid)
            child_checksums = node["target"]["node"]
            # Appends items in child_details with key as child_name
            # and value as list of child_swhid, child_checksums and child_path
            child_details[child_name] = [
                child_swhid,
                child_checksums,
                child_path,
            ]

    return child_details
