from typing import Any, Dict, Type

from ...models import Evaluator as EvaluatorModel
from ..evaluator import Evaluator, EvaluatorBackend, EvaluatorBackendT
from ..paths import SCHEMAS_PATH, resolve_path
from ..util import subclasses_dict


class EvaluatorLoader:
    evaluators: Dict[int, Evaluator] = {}

    @classmethod
    def get_evaluator(cls, id: int) -> Evaluator:
        try:
            return cls.evaluators[id]
        except Exception:
            raise KeyError(f"An evaluator with id {id} is not loaded.")

    @classmethod
    def list_evaluator_models(cls):
        return [evaluator.model for evaluator in cls.evaluators.values()]

    def __init__(self, step_size: float, offline_mode: bool):
        self._evaluator_backends = subclasses_dict(EvaluatorBackend)

    def load(self, evaluators: Dict[str, Any]):
        for id, settings in evaluators.items():
            self._load_evaluator(int(id), settings)

    def _get_evaluator_backend(self, class_name: str) -> Type[EvaluatorBackendT]:
        try:
            return self._evaluator_backends[class_name]
        except KeyError:
            raise KeyError(
                f"An evaluator backend with the classname {class_name} does not exist.")

    def _load_evaluator(self, id: int, settings: Dict[str, Any]) -> Evaluator:
        self.evaluators[id] = Evaluator(
            model=EvaluatorModel(id=id,
                                 name=settings["name"]),
            backend_class=self._get_evaluator_backend(settings["model_class"]),
            backend_file=resolve_path(settings["model_file"], SCHEMAS_PATH),
            width=settings["width"],
            height=settings["height"]
        )
