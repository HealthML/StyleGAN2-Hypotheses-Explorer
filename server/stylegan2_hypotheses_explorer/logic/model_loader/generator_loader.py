from functools import cached_property
from pathlib import Path
from typing import Any, Dict, Type

from ...models import Generator as GeneratorModel
from ...models import GeneratorSettings
from ..generator import Generator, GeneratorBackend, GeneratorBackendT
from ..paths import GENERATOR_SETTINGS_SCHEMA_PATH, SCHEMAS_PATH, resolve_path
from ..util import load, load_and_validate, subclasses_dict


class GeneratorLoader:
    generators: Dict[int, Generator] = {}

    @classmethod
    def get_generator(cls, id: int) -> Generator:
        try:
            return GeneratorLoader.generators[id]
        except KeyError:
            raise KeyError(f"A generator with id {id} is not loaded.")

    @classmethod
    def list_generator_models(cls):
        return [generator.model for generator in cls.generators.values()]

    def __init__(self, step_size: float, offline_mode: bool):
        self._generator_backends = subclasses_dict(GeneratorBackend)
        self._step_size = step_size
        self._offline_mode = offline_mode

    def load(self, generators: Dict[str, Any]):
        for id, settings in generators.items():
            self._load_generator(int(id), settings)

    def _get_generator_backend(self, class_name: str) -> Type[GeneratorBackendT]:
        try:
            return self._generator_backends[class_name]
        except KeyError:
            raise KeyError(
                f"A generator backend with the classname {class_name} does not exist.")

    @cached_property
    def _generator_settings_schema(self) -> Dict:
        return load(GENERATOR_SETTINGS_SCHEMA_PATH)

    def _get_generator_settings(self,
                                settings_path: Path,
                                layer_count: int):
        if not settings_path.exists():
            return GeneratorSettings(num_gen_styles_per_layer=3,
                                     use_same_styles_for_all_layers=True,
                                     reduce_number_of_layers_by=layer_count - 3)
        else:
            return GeneratorSettings.from_dict(load_and_validate(settings_path,
                                                                 self._generator_settings_schema))

    def _load_generator(self, id: int, settings: Dict[str, Any]) -> Generator:
        layer_count = settings["layer_count"]
        settings_path = resolve_path(settings["settings"], SCHEMAS_PATH)
        self.generators[id] = Generator(
            model=GeneratorModel(id=id,
                                 name=settings["name"],
                                 number_of_layers=layer_count,
                                 settings=self._get_generator_settings(settings_path,
                                                                       layer_count),
                                 step_size=self._step_size,
                                 offline_mode=self._offline_mode),
            backend_class=self._get_generator_backend(settings["model_class"]),
            backend_file=resolve_path(settings["model_file"], SCHEMAS_PATH),
            width=settings["width"],
            height=settings["height"],
            batch_size=settings["batch_size"],
            settings_cache=settings_path
        )
