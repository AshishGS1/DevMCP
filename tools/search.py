from fastmcp.exceptions import ToolError
from typing import Any
from services import embed, to_record
from db import get_client
from config import setting


#similarity search on records based on query string
async def simi_search(query: str, top_k: int =setting.top_k, thresh: float = setting.score_threshold) -> dict[str,Any]:
    """search top k similar records based on query."""
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