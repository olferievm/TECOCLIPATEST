from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

from app.config import HOST, PORT, SECRET_KEY, SESSION_MAX_AGE_SECONDS
from app.schema_generator import initialize_database
from routers.auth import router as auth_router
from routers.export import router as export_router
from routers.patients import router as patients_router
from routers.records import router as records_router


def create_app() -> FastAPI:
    app = FastAPI(title="Local Clinical Data Collection")
    app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, max_age=SESSION_MAX_AGE_SECONDS)
    app.mount("/static", StaticFiles(directory="static"), name="static")

    app.include_router(auth_router)
    app.include_router(records_router)
    app.include_router(patients_router)
    app.include_router(export_router)

    @app.on_event("startup")
    def _startup():
        initialize_database()

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=False)
