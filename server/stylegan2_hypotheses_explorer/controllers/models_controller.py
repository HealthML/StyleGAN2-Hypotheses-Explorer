from ..logic.model_loader import ModelLoader


def models_list_get():  # noqa: E501
    """List all generators and evaluators + their settings

     # noqa: E501


    :rtype: ModelsArray
    """
    return ModelLoader.list_all_models()
