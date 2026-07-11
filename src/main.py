from fastapi import FastAPI
from src.api.auth.routes import auth_router


app=FastAPI(title="simple fastapi app")

app.include_router(auth_router,prefix="/app/auth",tags=["authentication"])
