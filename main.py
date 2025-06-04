from fastapi import FastAPI
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.album import album_router
from routers.computer import computer_router
from routers.user import user_router

app = FastAPI()
app.title = "Mi primera aplicación con FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(album_router)
app.include_router(computer_router)
app.include_router(user_router)


@app.get("/", tags=['Home'])
def message():
    return "Hello, World!"

Base.metadata.create_all(bind=engine)

# python3 venv venv -> source venv/bin/activate -> pip install fastapi -> pip install uvicorn -> uvicorn main:app --reload --port 8000 --host 0.0.0.0 -> Deactivate