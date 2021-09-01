import json
from functools import cached_property
from pathlib import Path
from shutil import rmtree
from typing import List

from tqdm import tqdm

from ...models import ModelsArray
from ..evaluator import Evaluator
from ..generator import Generator
from ..image_batch import ImageBatch
from ..util import batched
from .styles_collector import StylesCollector


class Exporter:
    def __init__(self,
                 root_folder: Path,
                 evaluators: List[Evaluator],
                 generators: List[Generator]):
        rmtree(str(root_folder), ignore_errors=True)
        self._root_folder = root_folder / "api" / "v2"
        self._root_folder.mkdir(parents=True, exist_ok=True)
        self._generators = generators
        self._evaluators = evaluators

    def export(self):
        for generator in self._generators:
            self._export_generator(generator)
        models_folder = self._root_folder / "models" / "list"
        models_folder.parent.mkdir(parents=True, exist_ok=True)
        models_folder.write_text(json.dumps(ModelsArray([generator.model for generator in self._generators],
                                                        [evaluator.model for evaluator in self._evaluators]).to_dict()))

    def _export_generator(self, generator: Generator):
        collector = StylesCollector(generator.model)
        generator.backend
        pbar = tqdm()
        pbar.reset(total=collector.number_of_styles // generator.batch_size)
        for styles in batched(collector.styles(), generator.batch_size):
            imageBatch = ImageBatch(generator, styles)
            self._export_images(imageBatch)
            self._export_ratings(imageBatch)
            pbar.update()
        pbar.refresh()

    def _export_images(self, imageBatch: ImageBatch):
        image_paths = [self._generator_base_path / serialized_style
                       for serialized_style in imageBatch.serialized_styles]
        imageBatch.generate().export_images(image_paths)

    def _export_ratings(self, imageBatch: ImageBatch):
        for evaluator, base_path in zip(self._evaluators, self._evaluator_base_paths):
            rating_paths = [base_path / serialized_style
                            for serialized_style in imageBatch.serialized_styles]
            ratings = imageBatch.rate(evaluator)
            for rating_path, rating in zip(rating_paths, ratings):
                rating_path.write_text(str(rating))

    @cached_property
    def _generator_base_path(self) -> Path:
        generator_base_path = self._root_folder / "generator" / "generate"
        generator_base_path.mkdir(parents=True, exist_ok=True)
        return generator_base_path

    @cached_property
    def _evaluator_base_paths(self) -> List[Path]:
        evaluators_base_path = self._root_folder / "evaluator"
        evaluator_base_paths = [evaluators_base_path / str(evaluator.model.id) / "evaluate"
                                for evaluator in self._evaluators]
        for path in evaluator_base_paths:
            path.mkdir(parents=True, exist_ok=True)
        return evaluator_base_paths
