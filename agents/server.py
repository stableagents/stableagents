from fastapi import fastapi

import uvicorn
import json 


def server(agents, host="0.0.0.0", port=8000):
    app = FastAPI()
    router = APIRouter()

    @app.post("/test/agents")
    async def action():
        return {"message": "test"}
    
    @app.


uvicorn.run(app, host=host, port=port)
