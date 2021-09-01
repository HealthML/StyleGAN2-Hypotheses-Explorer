import math
from functools import cached_property
from typing import Iterable

import numpy as np

from ...models import Generator as GeneratorModel
from ...models import (StyleConfiguration, StyleConfigurationSingleStyle,
                       StyleConfigurationStyleArray)


class StylesCollector:
    def __init__(self, model: GeneratorModel):
        self._model = model
        self._num_layers = model.number_of_layers - \
            model.settings.reduce_number_of_layers_by

        self._create_target_style()

    @cached_property
    def number_of_styles(self):
        styles_in_layer = self._model.settings.num_gen_styles_per_layer

        num_style_pairs_in_layer = styles_in_layer * (styles_in_layer - 1) / 2
        steps_per_style_pair = math.ceil(1 / self._model.step_size) - 1
        num_style_configurations_in_layer = \
            styles_in_layer + steps_per_style_pair * num_style_pairs_in_layer
        num_style_arrays = num_style_configurations_in_layer ** self._num_layers

        num_single_styles = styles_in_layer * self._num_layers
        return num_style_arrays + num_single_styles

    def styles(self) -> Iterable[StyleConfiguration]:
        self._target_style.single_style = self._target_single_style
        self._target_style.style_array = None
        for _ in self._single_styles():
            yield StyleConfiguration.from_dict(self._target_style.to_dict())

        self._target_style.single_style = None
        self._target_style.style_array = self._target_style_array
        for _ in self._style_arrays():
            yield StyleConfiguration.from_dict(self._target_style.to_dict())

    def _create_target_style(self):
        self._target_style = StyleConfiguration()
        self._target_style_array = [StyleConfigurationStyleArray()
                                    for _ in range(self._num_layers)]
        self._target_single_style = StyleConfigurationSingleStyle()
        self._proportions = np.arange(self._model.step_size,
                                      1,
                                      self._model.step_size)

    def _single_styles(self) -> Iterable[None]:
        for layer in range(self._num_layers):
            self._target_single_style.layer = layer
            for style_id in range(self._model.settings.num_gen_styles_per_layer):
                self._target_single_style.id = style_id
                yield None

    def _style_arrays(self) -> Iterable[None]:
        return self._style_configurations_accross_layers_recurse(self._num_layers - 1)

    def _style_configurations_accross_layers_recurse(self, layer: int) -> Iterable[None]:
        for _ in self._style_configurations_in_layer(self._target_style_array[layer]):
            if layer == 0:
                yield None
            else:
                for _ in self._style_configurations_accross_layers_recurse(layer - 1):
                    yield None

    def _style_configurations_in_layer(self, target_style_configuration: StyleConfigurationStyleArray) -> Iterable[None]:
        for style1 in range(self._model.settings.num_gen_styles_per_layer):
            target_style_configuration.style1 = style1
            target_style_configuration.style2 = None
            target_style_configuration.proportion_style1 = None
            yield None
            for style2 in range(style1):
                target_style_configuration.style2 = style2
                for proportion_style1 in self._proportions:
                    target_style_configuration.proportion_style1 = proportion_style1
                    yield None
