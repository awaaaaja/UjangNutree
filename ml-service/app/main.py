import logging
from fastapi import FastAPI
from app.api.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="UjangNutree ML Service",
    description="Meal Recommendation System API",
    version="1.0.0",
)

app.include_router(router)