from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.database import engine
from app.api.v1.cards import router as cards_router
from app.api.v1.operations import router as operations_router
from app.api.v1.users import router as users_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Database schema is managed by Alembic
    yield
    
    # Close the database connection when the application shuts down
    await engine.dispose()
    
# initialize FastAPI app
app = FastAPI(lifespan=lifespan)

PROJECT_DIR = Path(__file__).parent
VUE_DIST_DIR = PROJECT_DIR / "frontend" / "dist"

if VUE_DIST_DIR.exists():
    app.mount("/assets", StaticFiles(directory=VUE_DIST_DIR / "assets"), name="vue-assets")


@app.get("/", include_in_schema=False)
def frontend() -> FileResponse:
    index_file = VUE_DIST_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)

# Connecting routers with prefix /api/v1
app.include_router(cards_router, prefix="/api/v1", tags=["cards"])
app.include_router(operations_router, prefix="/api/v1", tags=["operations"])
app.include_router(users_router, prefix="/api/v1", tags=["users"])
    
