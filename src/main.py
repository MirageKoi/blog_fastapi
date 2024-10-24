from fastapi import FastAPI

from src.adapters.database import Base, engine
from src.auth.routers import router as auth_router
from src.posts.routers import router as post_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(post_router)

Base.metadata.create_all(bind=engine)
