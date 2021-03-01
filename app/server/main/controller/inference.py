import logging
import os
import json
from typing import Tuple

import io
from PIL import Image 

import torch 
from torchvision import models,transforms


logger = logging.getLogger(__name__)


model_transforms = {
    "dense_net_1": transforms.Compose([transforms.Resize((523,500)),
                                       transforms.ToTensor(),
                                       transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                                      ])
}


class Inference:
    def __init__(self, model: models, classes: dict, transforms: transforms, device: str = 'cpu'):
        self.model = model
        self.classes = classes
        self.transforms = transforms
        self.device = device

    @classmethod
    def load_dense_net(cls, weights_path, classes_path):
        if not os.path.isfile(weights_path):
            raise FileNotFoundError(f"File does not exist: {weights_path}")
        elif not os.path.isfile(classes_path):
            raise FileNotFoundError(f"File does not exist: {classes_path}")
        else:
            # 1. Detect GPU, otherwise CPU
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

            # 2. Read and add classes
            with open(classes_path) as f:
                classes = json.load(f)

            # 3. Create Dense Net Model
            model = models.densenet121().to(device)
            model.classifier = torch.nn.Linear(model.classifier.in_features, len(classes))
            model.load_state_dict(torch.load(weights_path, map_location=device))
            model.eval()

            return cls(model, classes, transforms=model_transforms['dense_net_1'] ,device=device)

    def classify(self, image_bytes: bytes) -> Tuple[str, float]:
        if not self.model:
            raise ValueError("Uninitialized model")
        elif not self.classes:
            raise ValueError("Uninitialized classes")
        elif not self.transforms:
            raise ValueError("Uninitialized transforms")
        else:
            # 1. Convert bytes to image
            image = Image.open(io.BytesIO(image_bytes))

            # 2. Apply transformation to image
            image_tensor = self.transforms(image).unsqueeze(0)

            # 3. Perform inference
            output = self.model(image_tensor)
            score, pred = torch.max(output, 1)

            # 4. Convert output to readable classification
            pred = self.classes[str(pred.item())].title()

            return pred, score
