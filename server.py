from fastmcp import FastMCP
from db import lifespan
from tools.insert import insert_rec
from tools.fetch import get_rec, get_all_recs
from tools.delete import delete_rec
from tools.search import simi_search
from config import setting


mcp=FastMCP("DevMCP",lifespan=lifespan, tools=[insert_rec, get_rec, get_all_recs, delete_rec, simi_search])


if __name__ == "__main__":
    mcp.run(transport="http", host=setting.host, port=setting.port)