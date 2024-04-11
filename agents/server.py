import uvicorn
import json 
from typing import Generator, Union

from fastapi import Body, FastAPI, Request, Response, Websocket


def server(agents, host="0.0.0.0", port=8000):
    app = FastAPI()
    router = APIRouter()

    @app.post("/test/agents")
    async def action():
        return {"message": "test"}
    
    @app.


# uvicorn.run(app, host=host, port=port)
