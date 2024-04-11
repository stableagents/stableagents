from fastapi import fastapi

import uvicorn


def server(agents, host="0.0.0.0", port=8000):
    app = FastAPI()

    @app.post("/test/agents")
    async def action():
        return {"message": "test"}
