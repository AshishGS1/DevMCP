from mcp_app import mcp
from config import setting
import tools.insert
import tools.fetch
import tools.search
import tools.delete


if __name__ == "__main__":
    mcp.run(transport="http", host=setting.host, port=setting.port)