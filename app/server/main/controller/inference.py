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
    """A class to handle models inference

    Attributes:
        model (models): The model used to train the NN
        classes (dict): Classes of objects used in training (number to name)
        transforms (transforms): Transformations applied to images before training/classification
        device (str, optional): The device used for inference. Defaults to 'cpu'.
    """
    def __init__(self, model: models, classes: dict, transforms: transforms, device: str = 'cpu'):
        """The constructor for Inference class

        Args:
            model (models): The model used to train the NN
            classes (dict): Classes of objects used in training (number to name)
            transforms (transforms): Transformations applied to images before training/classification
            device (str, optional): The device used for inference. Defaults to 'cpu'.
        """
        self.model = model
        self.classes = classes
        self.transforms = transforms
        self.device = device

    @classmethod
    def load_dense_net(cls, weights_path: str, classes_path: str):
        """Creates an Inference object for Dense Net using the given weights
           and classes.

        Args:
            weights_path (str): Path to the trained weights (.pt)
            classes_path (str): Path to classes file (.json)

        Raises:
            FileNotFoundError: If the given path for weights_path or classes_path
                               is invalid.

        Returns:
            Inference: An initialized object
        """
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
        """Executes inference and classifies the object in the given image

        Args:
            image_bytes (bytes): Image in bytes format

        Raises:
            ValueError: If any of model, classes or transforms is falsy

        Returns:
            Tuple[str, float]: The classification and confidence
        """
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

            logger.debug("Detected %s with confidence %s", pred, score)

            return pred, score
