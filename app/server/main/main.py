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
    prefix="/api",
    #tags=["api"],
    #responses={418: {"description": "I'm a teapot"}},
)

'''
@app.get("/api")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
'''
