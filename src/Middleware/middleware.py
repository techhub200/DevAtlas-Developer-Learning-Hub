from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

logger = logging.getLogger("uvicorn.access")
logger.disabled = True

def register_middleware(app: FastAPI):

    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        print(
            f"{request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Time: {process_time:.4f}s"
        )

        return response
    


    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],      # Allowed frontend origins
        allow_credentials=True,   # Allow cookies/authorization
        allow_methods=["*"],      # Allow all HTTP methods
        allow_headers=["*"],      # Allow all headers
    )