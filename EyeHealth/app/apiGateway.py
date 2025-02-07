from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import redis
import jwt
import datetime
import logging
import random

# ================== Настройки ==================
DATABASE_URL = "postgresql://postgres:password@localhost/gatewaydb"
REDIS_URL = "redis://localhost:6379/0"
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
RATE_LIMIT = 5  # Лимит запросов в минуту

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)

app = FastAPI()

# ================== Логирование ==================
logging.basicConfig(filename="gateway.log", level=logging.INFO, format="%(asctime)s - %(message)s")


class LoggingService:
    @staticmethod
    def log_event(event: str):
        logging.info(event)


# ================== Аутентификация ==================
class AuthService:
    @staticmethod
    def create_token(user_id: str):
        payload = {"user_id": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")


# ================== Ограничение частоты ==================
class RateLimiter:
    @staticmethod
    def check_limit(user_id: str):
        key = f"rate_limit:{user_id}"
        count = redis_client.get(key)

        if count and int(count) >= RATE_LIMIT:
            raise HTTPException(status_code=429, detail="Too many requests")

        redis_client.incr(key)
        redis_client.expire(key, 60)  # Сбрасывается через минуту


# ================== Кэширование ==================
class CacheService:
    @staticmethod
    def get_cache(key: str):
        return redis_client.get(key)

    @staticmethod
    def set_cache(key: str, value: str, ttl: int = 60):
        redis_client.setex(key, ttl, value)


# ================== Балансировка нагрузки ==================
class LoadBalancer:
    services = ["http://service1.local", "http://service2.local", "http://service3.local"]

    @staticmethod
    def get_service():
        return random.choice(LoadBalancer.services)


# ================== Маршрутизация ==================
class RequestRouter:
    @staticmethod
    def route_request(endpoint: str):
        service_url = LoadBalancer.get_service()
        return f"{service_url}/{endpoint}"


# ================== API Gateway ==================
@app.middleware("http")
async def api_gateway(request: Request, call_next):
    token = request.headers.get("Authorization")

    if not token:
        raise HTTPException(status_code=401, detail="Authorization required")

    user_id = AuthService.verify_token(token)
    RateLimiter.check_limit(user_id)

    cache_key = f"cache:{request.url}"
    cached_response = CacheService.get_cache(cache_key)

    if cached_response:
        return cached_response

    response = await call_next(request)
    CacheService.set_cache(cache_key, str(response.body), 30)
    LoggingService.log_event(f"Request: {request.url} by {user_id}")

    return response


@app.get("/route/{endpoint}")
def route(endpoint: str):
    return {"redirect_to": RequestRouter.route_request(endpoint)}


@app.get("/token/{user_id}")
def get_token(user_id: str):
    return {"token": AuthService.create_token(user_id)}
