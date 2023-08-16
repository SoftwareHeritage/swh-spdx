from datetime import datetime

from spdx_tools.spdx.model import Actor, ActorType, CreationInfo


def set_creation_info(document_name: str) -> CreationInfo:
    """
    Contains information about the Tools and attributes used for creating SPDX document

    Args:
        document_name (str): Name of document

    Returns:
        creation_info (CreationInfo)
    """
    creation_info = CreationInfo(
        spdx_version="SPDX-2.3",
        spdx_id="SPDXRef-DOCUMENT",
        name=document_name,
        data_license="CC0-1.0",
        document_namespace="https://some.namespace",
        creators=[
            Actor(ActorType.ORGANIZATION, "SOFTWARE HERITAGE", "swh@example.com"),
            Actor(ActorType.TOOL, "swh-spdx"),
        ],
        created=datetime.now(),
    )
    return creation_info
