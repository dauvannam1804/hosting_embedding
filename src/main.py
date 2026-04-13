from fastapi import FastAPI
from src.api.routes import router
from src.core.config import settings

app = FastAPI(title="Embedding Service Professional")

# Include routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host=settings.host, port=settings.port, reload=True)
