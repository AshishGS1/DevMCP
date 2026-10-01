from fastmcp.server.lifespan import lifespan
from qdrant_client import AsyncQdrantClient
from fastmcp.exceptions import ToolError
from config import setting
from qdrant_client.models import VectorParams, Distance


client: AsyncQdrantClient | None = None

@lifespan
async def lifespan(server):
    #runs once at server start, to check for qdrant collection and create it if absent
    global client
    client = AsyncQdrantClient(url=setting.qdrant_url, api_key=setting.qdrant_api_key)
    try:
        if not await client.collection_exists(setting.collection):
            await client.create_collection(
                collection_name=setting.collection,
                vectors_config=VectorParams(size=setting.dims,distance=Distance.COSINE),
            )
        yield
    finally:
       client=None
       await client.close()

def get_client()->AsyncQdrantClient:
    if client is None:
        raise ToolError("Qdrant client is not initialised")
    return client