from fastapi import FastAPI

from app.db.session import init_db
from app.api.health import router as health_router
from app.api.tenders import router as tenders_router


app = FastAPI(
    title="223-FZ Education Tender Monitor",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():

    await init_db()


app.include_router(health_router)
app.include_router(tenders_router)
