from gql import gql


def get_query_content():
    """
    Constructs the initial GraphQL query to retrieve the content of a given SWHID.

    Args:
        None

    Returns:
        gql.Query: constructed gql query with hashes as parameters
    """
    query = gql(
        """
        query GetContent($sha1: String!, $sha256: String!, $sha1_git: String!, $blake2s256: String!) {  # noqa
                contentByHashes(
                  sha1: $sha1
                  sha256: $sha256
                  sha1_git: $sha1_git
                  blake2s256: $blake2s256
                ) {
                  data {
                       url
                       raw { text }
                  }
                }
              }
        """
    )
    return query


def get_query_children():
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
                  entries(first: 16, after: $cursor
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
                                sha1_git
                                blake2s256
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
