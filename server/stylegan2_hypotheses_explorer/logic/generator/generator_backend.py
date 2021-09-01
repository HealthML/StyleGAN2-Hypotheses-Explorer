from abc import ABC, abstractmethod
from base64 import b64decode
from io import BytesIO
from pathlib import Path
from typing import List, Tuple, TypeVar, Union

import torch
from PIL import Image

from ...models import Generator as GeneratorModel
from ..evaluator.evaluator_backend import EvaluatorBackendT


class GeneratorBackend(ABC):
    '''
    Imporatant: When subclassing GeneratorBackend, the subclass must be added to the __init__.py file in order to be usable from the models.json file.
    '''

    def __init__(self,
                 width: int,
                 height: int,
                 trained_model: Path,
                 batch_size: int,
                 cache_path: Path,
                 model: GeneratorModel):
        self.styles: List[List[torch.Tensor]] = None
        self.styles = self.styles
        self.width = width
        self.height = height
        self.trained_model = trained_model
        self.batch_size = batch_size
        self.dev = "cuda:0"
        self._cache_path = cache_path
        self.model = model

    @abstractmethod
    def generate_new_styles(self, model: GeneratorModel):
        pass

    @abstractmethod
    def generate_images(self, styles: List[Tuple[torch.Tensor, int]]) -> torch.Tensor:
        pass

    @property
    def cache_path(self) -> Path:
        self._cache_path.mkdir(parents=True, exist_ok=True)
        return self._cache_path

    @property
    def styles_cache_path(self) -> Path:
        return self.cache_path / "styles.pt"

    @property
    def settings_cache_path(self) -> Path:
        return self.cache_path / "settings.json"

    def _optimizer(self) -> Union[EvaluatorBackendT, None]:
        optimizer = self.model.settings.optimize_styles
        if optimizer is not None:
            from ..model_loader import ModelLoader
            optimizer = ModelLoader.get_evaluator(int(optimizer)).backend
        return optimizer

    def _styles_from_images(self) -> Union[List[Image.Image], None]:
        if self.model.settings.styles_from_images:
            BytesIO()
            return [Image.open(BytesIO(b64decode(image)))
                    for image in self.model.settings.styles_from_images]
        else:
            return None


GeneratorBackendT = TypeVar("GeneratorBackendT", bound=GeneratorBackend)
