from gql import gql

from swh.spdx.connection import set_connection


def get_query():
    """
    Constructs the initial GraphQL query to retrieve the directory entries of a given SWHID.

    Args:
        None

    Returns:
        gql.Query: constructed gql query with swhid and cursor as a parameters
    """
    query = gql(
        """
      query Getdir($swhid: SWHID!, $cursor: String) {
                directory(
                  swhid: $swhid
                ) {
                  swhid
                  entries(first: 12, after: $cursor
                  ){
                    totalCount
                    pageInfo {
                      endCursor
                      hasNextPage
                    }
                    edges {
                      node {
                        name { text }
                        target {
                          swhid
                          node {
                            ... on Content{
                              hashes{
                                sha1
                                sha256
                              }
                            }
                            ... on Directory{
                              id
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }

        """
    )
    return query


def get_child(dir_swhid: str, dire_name):
    """
    Retrieves the child details of a directory specified by its SWHID.

    Args:
        dir_swhid (str): The SWHID of the directory.
        dire_name (str): The name of the directory whose children details needs to be retrieved.

    Returns:
        Dict[str, List]: A dictionary containing the child details,
        where the keys are child names and the values is a list of swhid,
        checksums and directory path of child.
    """
    if not dir_swhid.split(":")[2] == "dir":
        raise ValueError(f"{dir_swhid} is not a valid directory SWHID")
    client = set_connection()
    has_next_page = True
    cursor = None
    # Initialize child details as empty dictionary
    child_details = {}
    while has_next_page:
        query = get_query()
        params = {"swhid": dir_swhid, "cursor": cursor}
        response = client.execute(query, params)
        page_info = response["directory"]["entries"]["pageInfo"]
        has_next_page = page_info["hasNextPage"]
        cursor = page_info["endCursor"]
        edges = response["directory"]["entries"]["edges"]
        for edge in edges:
            node = edge["node"]
            child_name = node["name"]["text"]
            child_path = f"{dire_name}/{child_name}"
            child_swhid = node["target"]["swhid"]
            child_checksums = node["target"]["node"]
            # Appends items in child_details with key as child_name
            # and value as list of child_swhid, child_checksums and child_path
            child_details[child_name] = [
                child_swhid,
                child_checksums,
                child_path,
            ]

    return child_details
