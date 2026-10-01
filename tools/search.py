from fastmcp.exceptions import ToolError
from typing import Any
from services import embed, to_record, parse_guid
from db import get_client
from config import setting
from qdrant_client.models import FieldCondition, MatchValue, Filter


#similarity search on records based on query string
async def simi_search(query: str, top_k: int =setting.top_k, 
                      thresh: float = setting.score_threshold) -> dict[str,Any]:
    """search top k similar records based on query. use filter records for exact parameters"""
    query=query.strip()
    if not  query:
        raise ToolError("query cannot be empty")
    if top_k<=0:
        raise ToolError("top k must be greater than 0")
    client= get_client()
    vector= await embed(query)
    res= await client.query_points(
        collection_name=setting.collection, 
        query=vector, limit=top_k, 
        score_threshold=thresh
    )
    return {"records":[to_record(p, has_score=True) for p in res.points],
            "count": len(res.points),}


async def filter_recs(role: str | None = None, skills: list[str] | None = None, 
                      cursor: str | None = None) -> dict[str,Any]:
    """filter records by exact parameters. use simi search for descriptive queries"""
    role = role.strip() if role else None
    skills=[s.strip() for s in (skills or []) if s and s.strip()]
    if not role and not skills:
         raise ToolError("Provide at least a role and/or skills.")
    conditions=[]
    if role:
        conditions.append(FieldCondition(key="role", match=MatchValue(value=role)))
    for s in skills:
        conditions.append(FieldCondition(key="skills", match=MatchValue(value=s)))
    offset = parse_guid(cursor) if cursor else None
    client = get_client()
    pts, next_offset = await client.scroll(
        collection_name=setting.collection,
        scroll_filter=Filter(must = conditions),
        limit = setting.page_size,
        offset = offset,
        with_payload = True,
        with_vectors = False)
    return{"records": [to_record(p) for p in pts],
           "matches": len(pts),
           "next_cursor": str(next_offset) if next_offset is not None else None}
