from pathlib import Path
from typing import List, Type

import torch

from ...models import Evaluator as EvaluatorModel
from ..backend_lazy_loader import BackendLazyLoader
from .evaluator_backend import EvaluatorBackendT


class Evaluator(BackendLazyLoader[EvaluatorBackendT]):
    def __init__(self,
                 model: EvaluatorModel,
                 backend_class: Type[EvaluatorBackendT],
                 backend_file: Path,
                 width: int,
                 height: int):
        super().__init__()
        self._model = model
        self._backend_class = backend_class
        self._backend_file = backend_file
        self._width = width
        self._height = height

    @property
    def model(self) -> EvaluatorModel:
        return self._model

    def rate(self, images: List[torch.Tensor]) -> List[float]:
        return self.backend.rate_image_batch(torch.stack(images)).squeeze(1).tolist()

    ############################################

    @property
    def max_allocated_backends(self) -> int:
        return 5

    def construct_backend(self) -> EvaluatorBackendT:
        return self._backend_class(self._width, self._height, self._backend_file)
