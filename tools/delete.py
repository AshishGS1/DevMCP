from mcp_app import mcp
from fastmcp.exceptions import ToolError
from typing import Any
from services import parse_guid
from db import get_client
from config import setting
from qdrant_client.models import Filter, FilterSelector

@mcp.tool(name= "Delete Records")
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

@mcp.tool(name= "Delete All Records (!caution)")
async def delete_all(confirm: bool) -> dict[str, Any]:
    if confirm:
        client = get_client()
        await client.delete(
            collection_name = setting.collection,
            points_selector = FilterSelector(filter=Filter),
            wait=True
        )
        return {"confirm": confirm,
                "deleted": True}
    else:
        return {"confirm": confirm,
                "deleted": False}