from fastmcp import FastMCP
from db import lifespan
from fastmcp.server.auth.providers.jwt import JWTVerifier
from config import setting
import logging
import json
from uuid import uuid4
from fastmcp.server.middleware import Middleware as MCPMiddleware, MiddlewareContext
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

verifier = JWTVerifier(
    public_key=setting.jwt_secret,   #despite the name,takes the HMAC secret
    issuer="devs-mcp-local",
    audience="devs-mcp",
    algorithm="HS256",
)

logg= logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class LogMiddleware(MCPMiddleware):
    async def on_request(self, context: MiddlewareContext, call_next):
        fcontx = context.fastmcp_context
        if fcontx and fcontx.request_context:
            request_id = fcontx.request_id
        else:
            # fallback correlation ID
            request_id = str(uuid4())

        body = context.message
        # body = message.model_dump(mode="json", by_alias=True)
        tool_name = (
            getattr(body, "name", None)
            if context.method == "tools/call"
            else None
        )

        logg.info(
            "%s",
            json.dumps({
                "request_id": request_id,
                "method": context.method,
                "tool_name": tool_name,
                "timestamp": context.timestamp.isoformat(),
                "body": body,
            }, default=str),
        )

        return await call_next(context)

mcp = FastMCP("DevMCP", lifespan=lifespan, auth=verifier)
mcp.add_middleware(LogMiddleware())

corsmiddlew= [
    Middleware(CORSMiddleware,
               allow_origins=["*"],
               allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
               allow_headers=["mcp-protocol-version",
                              "mcp-session-id",
                              "Authorization",
                              "Content-Type",],
               expose_headers=["mcp-session-id"],
               allow_credentials=True
               )
]

app= mcp.http_app(middleware=corsmiddlew)