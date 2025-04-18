# FastAPI main entrypoint
from fastapi import FastAPI
from app.api import indicators

app = FastAPI(
    title="Are U Query Ous",
    description="API for Are U Query Ous application",
    version="1.0.0"
)

# Conectamos el router con un "prefix" para agrupar las rutas
app.include_router(indicators.router, 
                   prefix="/indicators",
                     tags=["Indicators"])