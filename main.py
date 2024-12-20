from api.endpoints import router
from fastapi import FastAPI

app = FastAPI()

# Include API routes
app.include_router(router)
