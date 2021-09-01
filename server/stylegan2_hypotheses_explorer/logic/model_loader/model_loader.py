from ...models import ModelsArray
from ..evaluator import Evaluator
from ..generator import Generator
from ..paths import MODELS_PATH, MODELS_SCHEMA_PATH
from ..util import load_and_validate
from .evaluator_loader import EvaluatorLoader
from .generator_loader import GeneratorLoader


class ModelLoader:
    @classmethod
    def get_generator(cls, id: int) -> Generator:
        return GeneratorLoader.get_generator(id)

    @classmethod
    def get_evaluator(cls, id: int) -> Evaluator:
        return EvaluatorLoader.get_evaluator(id)

    @classmethod
    def list_all_models(cls) -> ModelsArray:
        return ModelsArray(
            GeneratorLoader.list_generator_models(),
            EvaluatorLoader.list_evaluator_models()
        )

    def __init__(self, step_size: float, offline_mode: bool):
        self._step_size = step_size
        self._offline_mode = offline_mode

    def load_models(self):
        models = load_and_validate(MODELS_PATH,
                                   MODELS_SCHEMA_PATH)
        EvaluatorLoader(self._step_size,
                        self._offline_mode).load(models["evaluators"])
        GeneratorLoader(self._step_size,
                        self._offline_mode).load(models["generators"])
