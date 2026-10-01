from sentence_transformers import SentenceTransformer
from config import setting
import asyncio
from resources.guidnamespace import DEV_NAMESPACE
from qdrant_client.models import PointStruct
from typing import Any
import uuid
from fastmcp.exceptions import ToolError

model=SentenceTransformer(setting.model_name)


def get_embed_text(role: str, skills: list[str], description: str) -> str:
    return f"Role: {role}. Skills: {', '.join(skills)}. Description: {description}"


async def embed(text:str) -> list[float]:
    vector = await asyncio.to_thread(model.encode, text, normalize_embeddings=True)
    return vector.tolist()


#unique guid for each dev id in record, updates existing record if duplicate entry is made
def guid_for_dev(id:int)->uuid.UUID:
    return uuid.uuid5(DEV_NAMESPACE,f"dev:{id}")


def to_record(point: PointStruct, has_score: bool = False) -> dict[str, Any]:
    rec={"guid": str(point.id), **(point.payload or{})}
    if has_score:
        rec["score"]=point.score
    return rec


def parse_guid(val: str) -> uuid.UUID:
    try:
        return uuid.UUID(val)
    except (ValueError, AttributeError):
        raise ToolError(f"Invalid guid: {val}")