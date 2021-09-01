from functools import cached_property
from typing import List

from cachetools import LRUCache
from torch import Tensor

from ...models import StyleConfiguration
from ..evaluator import Evaluator
from ..generator import Generator
from ..serialize_style import serialize_style
from .sprite_map import SpriteMap

MAX_CACHED_IMAGES = 1000


class ImageBatch:
    image_cache = LRUCache(MAX_CACHED_IMAGES)
    ratings_cache = LRUCache(MAX_CACHED_IMAGES)

    def __init__(self, generator: Generator, styles: List[StyleConfiguration]):
        self._styles = styles
        self._generator = generator

    def generate(self) -> SpriteMap:
        return SpriteMap(self._images)

    @cached_property
    def serialized_styles(self) -> List[str]:
        return [serialize_style(style, self._generator.model) for style in self._styles]

    def ratings_cache_key(self, evaluator: Evaluator, serialized_style: str):
        return str(evaluator.model.id) + serialized_style

    def rate(self, evaluator: Evaluator) -> List[float]:
        ratings = [None for _ in range(len(self._images))]
        non_cached_rating_indices = []
        non_cached_images = []
        for index, serialized_style in zip(range(len(self._images)), self.serialized_styles):
            try:
                rating = self.ratings_cache[self.ratings_cache_key(evaluator,
                                                                   serialized_style)]
                ratings[index] = rating
            except KeyError:
                non_cached_images.append(self._images[index])
                non_cached_rating_indices.append(index)
        if non_cached_images:
            non_cached_ratings = evaluator.rate(non_cached_images)
            for index, rating in zip(non_cached_rating_indices, non_cached_ratings):
                self.ratings_cache[self.ratings_cache_key(evaluator,
                                                          self.serialized_styles[index])] = rating
                ratings[index] = rating
        return ratings

    @cached_property
    def _images(self) -> List[Tensor]:
        images = [None for _ in range(len(self._styles))]
        non_cached_image_indices = []
        non_cached_styles = []
        for index, serialized_style in zip(range(len(self._styles)), self.serialized_styles):
            try:
                image = self.image_cache[serialized_style]
                images[index] = image
            except KeyError:
                non_cached_styles.append(self._styles[index])
                non_cached_image_indices.append(index)
        if non_cached_styles:
            non_cached_images = self._generator.generate_images(
                non_cached_styles)
            for index, image in zip(non_cached_image_indices, non_cached_images):
                self.image_cache[self.serialized_styles[index]] = image
                images[index] = image
        return images

    @classmethod
    def invalidate_cache(cls, generator: Generator):
        cls.image_cache.clear()
        cls.ratings_cache.clear()
