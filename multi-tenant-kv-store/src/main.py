from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST,Gauge
from prometheus_client.exposition import start_http_server
from starlette.middleware.base import BaseHTTPMiddleware
from src.config import settings
from src.routers import auth, kv
import uvicorn
from asyncio import create_task
import asyncio
from huey import RedisHuey
import huey
import logging
from src.services.tasks import huey, get_pending_task_count

logger = logging.getLogger(__name__)

# Metrics Definitions
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("http_request_latency_seconds", "HTTP Request Latency", ["method", "endpoint"])
TASK_QUEUE_SIZE = Gauge("task_queue_size", "Number of tasks in Huey queue")  


class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        endpoint = request.url.path
        with REQUEST_LATENCY.labels(method=method, endpoint=endpoint).time():
            response = await call_next(request)
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=response.status_code).inc()
        return response
    
async def update_task_queue_size(huey_instance: RedisHuey):
    while True:
        try:
            queue_size = get_pending_task_count()  
            TASK_QUEUE_SIZE.set(queue_size)            
        except Exception as e:
            logger.warning(f"Failed to update task queue size: {e}")
        await asyncio.sleep(5)  

def create_app() -> FastAPI:
    app = FastAPI(
        title="Multi-tenant Key-Value Store",
        version="1.0.0",
        debug=False
        # debug=settings.API_DEBUG
    )

    @app.get("/")
    async def root():
        return {"message": "The app is running"}
    
    # Health check
    @app.get("/health")
    async def health_check():
        return {"status": "ok"}
    
    
    @app.get("/metrics")
    async def metrics():
        return  Response (content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
    
    async def simulate_task_queue():
        while True:
            TASK_QUEUE_SIZE.inc(1)  
            await asyncio.sleep(10)

    @app.on_event("startup")
    async def startup_event():
      create_task(update_task_queue_size(huey_instance=huey))

   
    app.add_middleware(PrometheusMiddleware)

    app.include_router(auth.router)
    app.include_router(kv.router)
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("src.main:app", host=settings.API_HOST, port=settings.API_PORT, workers=2, reload=False)
