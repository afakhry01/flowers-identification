import base64

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from controller.inference import Inference


router = APIRouter(
    prefix="/flowers",
    #tags=["flowers"],
    responses={404: {"description": "Not found"}},
)


inferrer = Inference.load_dense_net('resources/plants_classification_cnn_dense_100_epochs.pt',
                                    'resources/cat_to_name.json'
                                   )


class Item(BaseModel):
    image: str


@router.post("/classify/")
async def classify_item(item: Item):
    try:
        pred, score = inferrer.classify(base64.b64decode(item.image))
        return {
            "classification": pred,
            "confidence": score
        }
    except ValueError:
        raise HTTPException(
            status_code=500, detail="Cannot get value"
        )
