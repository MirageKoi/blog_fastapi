from fastapi import FastAPI

from src.adapters.database import Base, engine
from src.analytics.routers import router as analytics_router
from src.auth.routers import router as auth_router
from src.posts.routers import router as post_router

app = FastAPI(root_path="/api/v1")

app.include_router(auth_router)
app.include_router(post_router)
app.include_router(analytics_router)

Base.metadata.create_all(bind=engine)
