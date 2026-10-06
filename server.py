from mcp_app import app
from config import setting
import tools.insert
import tools.fetch
import tools.search
import tools.delete


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=setting.host, port=setting.port)