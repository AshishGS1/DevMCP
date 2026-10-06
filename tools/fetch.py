from mcp_app import mcp
from fastmcp.exceptions import ToolError
from typing import Any
from services import to_record, parse_guid
from db import get_client
from config import setting
from models.developer import MultiRecResponse

@mcp.tool(name= "GetRecord")
async def get_rec(guid: str) -> dict[str, Any]:
    """get a developer record from the Devs collection by guid."""
    guid = parse_guid(guid)
    client = get_client()
    result = await client.retrieve(
        collection_name=setting.collection,
        ids=[guid]
    )
    if not result or not result[0]:
        raise ToolError(f"Record with guid '{guid}' not found.")
    return to_record(result[0])

@mcp.tool(name= "GetAllRecords")
async def get_all_recs(cursor: str | None = None) -> MultiRecResponse:
    """get all records from Devs collection upto page size. returns next cursor if size exceeded"""
    offset= parse_guid(cursor) if cursor else None
    client= get_client()
    res, offset= await client.scroll(collection_name=setting.collection, offset=offset, limit=setting.page_size)
    return MultiRecResponse(records=[to_record(p) for p in res], 
                            count= len(res),
                            next_cursor = str(offset) if offset else None)