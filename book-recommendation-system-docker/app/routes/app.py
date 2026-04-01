from fastapi import FastAPI

from app.db.database import Base, engine
from app.core.rate_limit import rate_limit_middleware
from app.routes.auth import router as auth_router
from app.routes.recommendation import router as recommendation_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Recommendation API")

app.middleware("http")(rate_limit_middleware)

app.include_router(auth_router)
app.include_router(recommendation_router)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)