from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeVar

import torch


class EvaluatorBackend(ABC):
    def __init__(self, width: int, height: int, trained_model: Path):
        self.width = width
        self.height = height
        self.trained_model = trained_model

    @abstractmethod
    def rate_image_batch(image_batch: torch.Tensor, enable_grad: bool = False) -> torch.Tensor:
        pass

    @abstractmethod
    def rate_style_batch(image_batch: torch.Tensor, enable_grad: bool = False) -> torch.Tensor:
        pass


EvaluatorBackendT = TypeVar("EvaluatorBackendT", bound=EvaluatorBackend)
