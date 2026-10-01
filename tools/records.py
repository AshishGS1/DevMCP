import uuid
from qdrant_client.models import PointStruct
from fastmcp.exceptions import ToolError
from models.developer import Dev
from typing import Any
from services import embed, get_embed_text, to_record, parse_guid, guid_for_dev
from db import get_client
from config import setting


#tools:
async def insert_rec(dev: Dev) -> dict[str, Any]:
    """insert a developer record into the Devs collection. assigns unique guid."""
    name, role, description = dev.name.strip(), dev.role.strip(), dev.description.strip()
    skills = [s.strip() for s in dev.skills if s and s.strip()]
    if not name:
        raise ToolError("'name' must not be empty.")
    if not role:
        raise ToolError("'role' must not be empty.")
    if not description:
        raise ToolError("'description' must not be empty.")
 
    client = get_client()
    guid = guid_for_dev(dev.id)
    vector = await embed(get_embed_text(role, skills, description))
    payload=dev.model_dump()
    await client.upsert(
        collection_name=setting.collection,
        points=[PointStruct(id=guid, vector=vector, payload=payload)],
    )
    return {"guid": guid, **payload}


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


async def get_all_recs(cursor: str | None = None) -> dict[str,Any]:
    """get all records from Devs collection upto page size. returns next cursor if size exceeded"""
    offset= parse_guid(cursor) if cursor else None
    client= get_client()
    res, offset= await client.scroll(collection_name=setting.collection, offset=offset, limit=setting.page_size)
    return {"records":[to_record(p) for p in res], 
            "count": len(res),
            "next_cursor": str(offset) if offset else None}
