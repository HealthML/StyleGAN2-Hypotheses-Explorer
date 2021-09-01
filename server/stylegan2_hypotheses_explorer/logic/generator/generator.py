import json
from pathlib import Path
from typing import List, Type

import torch

from ...models import Generator as GeneratorModel
from ...models import GeneratorSettings, StyleConfiguration
from ..backend_lazy_loader import BackendLazyLoader
from ..paths import CACHE_PATH
from .generator_backend import GeneratorBackendT


class Generator(BackendLazyLoader[GeneratorBackendT]):
    def __init__(self,
                 model: GeneratorModel,
                 backend_class: Type[GeneratorBackendT],
                 backend_file: Path,
                 width: int,
                 height: int,
                 batch_size: int,
                 settings_cache: Path):
        super().__init__()
        self._model = model
        self._backend_class = backend_class
        self._backend_file = backend_file
        self._width = width
        self._height = height
        self._batch_size = batch_size
        self._settings_cache = settings_cache

    @property
    def batch_size(self) -> int:
        return self._batch_size

    @property
    def model(self) -> GeneratorModel:
        return self._model

    def generate_new_styles(self, settings: GeneratorSettings):
        self.settings_cache.write_text(json.dumps(settings.to_dict(),
                                                  indent=4))
        self.model.settings = settings
        from ..image_batch import ImageBatch
        ImageBatch.invalidate_cache(self)
        if self.backend_is_allocated:
            self.backend.generate_new_styles(self.model)

    def generate_images(self, styles: List[StyleConfiguration]) -> torch.Tensor:
        return self.backend.generate_images(styles)

    ########################################

    @property
    def settings_cache(self):
        self._settings_cache.parent.mkdir(parents=True, exist_ok=True)
        return self._settings_cache

    @property
    def max_allocated_backends(self) -> int:
        return 1

    def construct_backend(self) -> GeneratorBackendT:
        styles_cache_path = CACHE_PATH / \
            "generators" / "styles" / str(self.model.id)
        return self._backend_class(self._width,
                                   self._height,
                                   self._backend_file,
                                   self._batch_size,
                                   styles_cache_path,
                                   self.model)
