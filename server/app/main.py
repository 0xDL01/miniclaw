from fastapi import FastAPI
from server.app.routes.nodes import router as nodes_router
from server.app.routes.tasks import router as tasks_router

app = FastAPI(title="MiniClaw Brain")

app.include_router(nodes_router, prefix="/nodes", tags=["nodes"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])


@app.get("/")
def root():
    return {"status": "MiniClaw brain running"}