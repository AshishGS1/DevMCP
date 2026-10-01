from fastmcp import FastMCP
from db import lifespan
from tools.records import insert_rec, get_rec, get_all_recs
from tools.search import simi_search
from config import setting


mcp=FastMCP("DevMCP",lifespan=lifespan, tools=[insert_rec, get_rec, get_all_recs, simi_search])

if __name__ == "__main__":
    mcp.run(transport="http", host=setting.host, port=setting.port)