from typing import Optional
from logging.config import dictConfig

from fastapi import FastAPI
from controller.log import log_config


dictConfig(log_config)
app = FastAPI()


@app.get("/api")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
