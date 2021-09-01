# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from ..util import deserialize_model
from .base_model_ import Base_Model
from .style_configuration import StyleConfiguration  # noqa: F401,E501


class EvaluateImagesBatch(Base_Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, generator_id: int = None, styles: List[StyleConfiguration] = None):  # noqa: E501
        """EvaluateImagesBatch - a model defined in Swagger

        :param generator_id: The generator_id of this EvaluateImagesBatch.  # noqa: E501
        :type generator_id: int
        :param styles: The styles of this EvaluateImagesBatch.  # noqa: E501
        :type styles: List[StyleConfiguration]
        """
        self.swagger_types = {
            'generator_id': int,
            'styles': List[StyleConfiguration]
        }

        self.attribute_map = {
            'generator_id': 'generatorId',
            'styles': 'styles'
        }
        self._generator_id = generator_id
        self._styles = styles

    @classmethod
    def from_dict(cls, dikt) -> 'EvaluateImagesBatch':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The EvaluateImagesBatch of this EvaluateImagesBatch.  # noqa: E501
        :rtype: EvaluateImagesBatch
        """
        return deserialize_model(dikt, cls)

    @property
    def generator_id(self) -> int:
        """Gets the generator_id of this EvaluateImagesBatch.


        :return: The generator_id of this EvaluateImagesBatch.
        :rtype: int
        """
        return self._generator_id

    @generator_id.setter
    def generator_id(self, generator_id: int):
        """Sets the generator_id of this EvaluateImagesBatch.


        :param generator_id: The generator_id of this EvaluateImagesBatch.
        :type generator_id: int
        """
        if generator_id is None:
            raise ValueError("Invalid value for `generator_id`, must not be `None`")  # noqa: E501

        self._generator_id = generator_id

    @property
    def styles(self) -> List[StyleConfiguration]:
        """Gets the styles of this EvaluateImagesBatch.


        :return: The styles of this EvaluateImagesBatch.
        :rtype: List[StyleConfiguration]
        """
        return self._styles

    @styles.setter
    def styles(self, styles: List[StyleConfiguration]):
        """Sets the styles of this EvaluateImagesBatch.


        :param styles: The styles of this EvaluateImagesBatch.
        :type styles: List[StyleConfiguration]
        """
        if styles is None:
            raise ValueError("Invalid value for `styles`, must not be `None`")  # noqa: E501

        self._styles = styles