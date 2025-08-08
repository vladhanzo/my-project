from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api import api_router
from app.api import ws  # WebSocket router

app = FastAPI(
    title="Assembly Tracker",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Подключение всех маршрутов
app.include_router(auth_router)
app.include_router(api_router)
app.include_router(ws.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
