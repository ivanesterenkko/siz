from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache

from redis import asyncio as aioredis

from app.db import delete_tables, create_tables
from app.customers.router import router as customer_router

from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):

    await delete_tables()
    await create_tables()
    redis = aioredis.from_url(
        settings.redis_url,
        encoding="utf8",
        decode_responses=True
        )
    app.state.redis = redis
    FastAPICache.init(RedisBackend(redis), prefix="cache")

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(customer_router)

origins = [
    "http://localhost:8000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie",
                   "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)
