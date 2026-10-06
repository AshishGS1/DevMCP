from mcp_app import mcp
from fastmcp.exceptions import ToolError
from typing import Any
from services import embed, to_record, parse_guid
from db import get_client
from config import setting
from qdrant_client.models import FieldCondition, MatchValue, Filter
from models.developer import SimiSearchResponse, MultiRecResponse

@mcp.tool(name= "SimilaritySearch")
async def simi_search(query: str, 
                      top_k: int =setting.top_k, 
                      thresh: float = setting.score_threshold) -> SimiSearchResponse:
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
        query= vector, 
        limit= top_k, 
        score_threshold= thresh
    )
    return SimiSearchResponse(records= [to_record(p, has_score=True) for p in res.points],
                              count= len(res.points))

@mcp.tool(name= "FilterRecords")
async def filter_recs(role: str | None = None, 
                      skills: list[str] | None = None, 
                      cursor: str | None = None) -> MultiRecResponse:
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
    res, offset = await client.scroll(
        collection_name=setting.collection,
        scroll_filter=Filter(must = conditions),
        limit = setting.page_size,
        offset = offset,
        with_payload = True,
        with_vectors = False
    )
    return MultiRecResponse(records=[to_record(p) for p in res], 
                            count= len(res),
                            next_cursor = str(offset) if offset else None)
