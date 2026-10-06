from mcp_app import mcp
from fastmcp.exceptions import ToolError
from typing import Any
from services import parse_guid
from db import get_client
from config import setting
from qdrant_client.models import Filter, FilterSelector

@mcp.tool(name= "DeleteRecords")
async def delete_rec(guid: str) -> dict[str,Any]:
    """delete a record by guid"""
    guid = parse_guid(guid)
    client = get_client()
    res = await client.retrieve(
        collection_name=setting.collection,
        ids=[guid]
    )
    if not res:
        raise ToolError(f"RecordWithGuid '{guid}' not found.")
    await client.delete(
        collection_name=setting.collection,
        points_selector=[guid],
        wait=True
    )
    return {"guid": guid,
            "deleted": True}

@mcp.tool(name= "DeleteAllRecords")
async def delete_all(confirm: bool) -> dict[str, Any]:
    """CAUTION: Deleting all records is irreversible"""
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