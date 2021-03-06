# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from ..util import deserialize_model
from .base_model_ import Base_Model
from .evaluator import Evaluator  # noqa: F401,E501
from .generator import Generator  # noqa: F401,E501


class ModelsArray(Base_Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, generators: List[Generator] = None, evaluators: List[Evaluator] = None):  # noqa: E501
        """ModelsArray - a model defined in Swagger

        :param generators: The generators of this ModelsArray.  # noqa: E501
        :type generators: List[Generator]
        :param evaluators: The evaluators of this ModelsArray.  # noqa: E501
        :type evaluators: List[Evaluator]
        """
        self.swagger_types = {
            'generators': List[Generator],
            'evaluators': List[Evaluator]
        }

        self.attribute_map = {
            'generators': 'generators',
            'evaluators': 'evaluators'
        }
        self._generators = generators
        self._evaluators = evaluators

    @classmethod
    def from_dict(cls, dikt) -> 'ModelsArray':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ModelsArray of this ModelsArray.  # noqa: E501
        :rtype: ModelsArray
        """
        return deserialize_model(dikt, cls)

    @property
    def generators(self) -> List[Generator]:
        """Gets the generators of this ModelsArray.


        :return: The generators of this ModelsArray.
        :rtype: List[Generator]
        """
        return self._generators

    @generators.setter
    def generators(self, generators: List[Generator]):
        """Sets the generators of this ModelsArray.


        :param generators: The generators of this ModelsArray.
        :type generators: List[Generator]
        """
        if generators is None:
            raise ValueError("Invalid value for `generators`, must not be `None`")  # noqa: E501

        self._generators = generators

    @property
    def evaluators(self) -> List[Evaluator]:
        """Gets the evaluators of this ModelsArray.


        :return: The evaluators of this ModelsArray.
        :rtype: List[Evaluator]
        """
        return self._evaluators

    @evaluators.setter
    def evaluators(self, evaluators: List[Evaluator]):
        """Sets the evaluators of this ModelsArray.


        :param evaluators: The evaluators of this ModelsArray.
        :type evaluators: List[Evaluator]
        """
        if evaluators is None:
            raise ValueError("Invalid value for `evaluators`, must not be `None`")  # noqa: E501

        self._evaluators = evaluators
