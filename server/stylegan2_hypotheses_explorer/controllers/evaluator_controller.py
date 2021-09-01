import connexion

from ..logic.image_batch import ImageBatch
from ..logic.model_loader import ModelLoader
from ..models.evaluate_images_batch import EvaluateImagesBatch  # noqa: E501


def evaluator_evaluator_id_evaluate_post(body, evaluator_id):  # noqa: E501
    """Evaluate images from mixed styles and return them in order

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param evaluator_id: 
    :type evaluator_id: int

    :rtype: List[float]
    """
    if connexion.request.is_json:
        imageBatch = EvaluateImagesBatch.from_dict(
            connexion.request.get_json())

    evaluator = ModelLoader.get_evaluator(evaluator_id)
    generator = ModelLoader.get_generator(imageBatch.generator_id)
    return ImageBatch(generator, imageBatch.styles).rate(evaluator)


def evaluator_evaluator_id_evaluate_style_get(evaluator_id, style):  # noqa: E501
    """Get the rating of a generated image

     # noqa: E501

    :param evaluator_id: 
    :type evaluator_id: int
    :param style: 
    :type style: str

    :rtype: float
    """
    raise Exception("Unsupported")
