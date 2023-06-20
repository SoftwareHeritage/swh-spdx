import logging
from typing import Dict, List

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

transport = AIOHTTPTransport(url="https://archive.softwareheritage.org/graphql/")

client = Client(transport=transport, fetch_schema_from_transport=True)


def get_initial_query(dir_swhid: str) -> str:
    """
    Constructs the initial GraphQL query to retrieve the directory entries of a given SWHID.

    Args:
        dir_swhid (str): The SWHID of the directory.

    Returns:
        str: The constructed GraphQL query in string format.
    """
    query = f"""
        query Getdir {{
          directory(
            swhid: "{dir_swhid}"
          ) {{
            swhid
            entries(first: 12) {{
              totalCount
              pageInfo {{
                endCursor
              }}
              edges {{
                node {{
                  name {{ text }}
                  target {{
                    swhid
                    node {{
                      ... on Content{{
                        hashes{{
                          sha1
                          sha256
                        }}
                      }}
                      ... on Directory{{
                        id
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        """
    return query


def get_query_with_cursor(dir_swhid: str, cursor: str) -> str:
    """
    Constructs a GraphQL query to retrieve directory entries with a specified cursor.

    Args:
        dir_swhid (str): The SWHID of the directory.
        cursor (str): The cursor value for pagination.

    Returns:
        str: The constructed GraphQL query in string format.
    """
    query = f"""
        query Getdir {{
          directory(
            swhid: "{dir_swhid}"
          ) {{
            swhid
            entries(first: 12, after: "{cursor}") {{
              totalCount
              pageInfo {{
                endCursor
              }}
              edges {{
                node {{
                  name {{ text }}
                  target {{
                    swhid
                    node {{
                      ... on Content{{
                        hashes{{
                          sha1
                          sha256
                        }}
                      }}
                      ... on Directory{{
                        id
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        """
    return query


def get_child(dir_swhid: str) -> Dict[str, List]:
    """
    Retrieves the child details of a directory specified by its SWHID.

    Args:
        dir_swhid (str): The SWHID of the directory.

    Returns:
        Dict[str, List]: A dictionary containing the child details,
        where the keys are child names and the values are child SWHIDs and checksums.
    """

    try:
        result = client.execute(gql(get_initial_query(dir_swhid)))
        child_details = {}
        edges = result["directory"]["entries"]["edges"]
        for edge in edges:
            node = edge["node"]
            child_name = node["name"]["text"]
            child_swhid = node["target"]["swhid"]
            child_checksums = node["target"]["node"]
            child_details[child_name] = [child_swhid, child_checksums]
        while result["directory"]["entries"]["pageInfo"]["endCursor"] is not None:
            new_cursor = result["directory"]["entries"]["pageInfo"]["endCursor"]
            try:
                result = client.execute(
                    gql(get_query_with_cursor(dir_swhid, new_cursor))
                )
            except Exception as e:
                logging.exception(e)

            edges = result["directory"]["entries"]["edges"]
            for edge in edges:
                node = edge["node"]
                child_name = node["name"]["text"]
                child_swhid = node["target"]["swhid"]
                child_checksums = node["target"]["node"]
                child_details[child_name] = [child_swhid, child_checksums]

        return child_details
    except Exception as e:
        logging.exception(e)
        return {}
