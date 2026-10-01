from fastmcp.exceptions import ToolError
from typing import Any
from services import parse_guid
from db import get_client
from config import setting


async def delete_rec(guid: str) -> dict[str,Any]:
    """delete a record by guid"""
    guid = parse_guid(guid)
    client = get_client()
    res = await client.retrieve(
        collection_name=setting.collection,
        ids=[guid]
    )
    if not res:
        raise ToolError(f"Record with guid '{guid}' not found.")
    await client.delete(
        collection_name=setting.collection,
        points_selector=[guid],
        wait=True
    )
    return {"guid": guid,
            "deleted": True}