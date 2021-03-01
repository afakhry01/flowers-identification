from typing import Optional
from logging.config import dictConfig

from fastapi import FastAPI
from controller.log import log_config
from controller.inference import Inference
from router import flowers

dictConfig(log_config)
app = FastAPI()

app.include_router(
    flowers.router,
    prefix="/api"
)
