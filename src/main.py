from fastapi import FastAPI
from src.routers.accounts import router as accounts_router

app = FastAPI(title="SecureBank API")
app.include_router(accounts_router)