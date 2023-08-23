from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport


def get_graphql_client():
    """
    Sets connection to the Graphql server of Software heritage

    Args:
        None

    Returns:
        gql.Client: graphql client through which query will be executed
    """
    transport = AIOHTTPTransport(url="https://archive.softwareheritage.org/graphql/")
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client
