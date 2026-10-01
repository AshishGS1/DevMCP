from qdrant_client.models import PointStruct
from fastmcp.exceptions import ToolError
from models.developer import Dev
from typing import Any
from services import embed, get_embed_text, to_record, parse_guid, guid_for_dev
from db import get_client
from config import setting


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
    return {"guid": str(guid), **payload}





                        
