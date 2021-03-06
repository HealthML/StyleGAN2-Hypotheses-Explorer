# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from ..util import deserialize_model
from .base_model_ import Base_Model
from .style_configuration_single_style import \
    StyleConfigurationSingleStyle  # noqa: F401,E501
from .style_configuration_style_array import \
    StyleConfigurationStyleArray  # noqa: F401,E501


class StyleConfiguration(Base_Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, style_array: List[StyleConfigurationStyleArray] = None, single_style: StyleConfigurationSingleStyle = None):  # noqa: E501
        """StyleConfiguration - a model defined in Swagger

        :param style_array: The style_array of this StyleConfiguration.  # noqa: E501
        :type style_array: List[StyleConfigurationStyleArray]
        :param single_style: The single_style of this StyleConfiguration.  # noqa: E501
        :type single_style: StyleConfigurationSingleStyle
        """
        self.swagger_types = {
            'style_array': List[StyleConfigurationStyleArray],
            'single_style': StyleConfigurationSingleStyle
        }

        self.attribute_map = {
            'style_array': 'styleArray',
            'single_style': 'singleStyle'
        }
        self._style_array = style_array
        self._single_style = single_style

    @classmethod
    def from_dict(cls, dikt) -> 'StyleConfiguration':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The StyleConfiguration of this StyleConfiguration.  # noqa: E501
        :rtype: StyleConfiguration
        """
        return deserialize_model(dikt, cls)

    @property
    def style_array(self) -> List[StyleConfigurationStyleArray]:
        """Gets the style_array of this StyleConfiguration.


        :return: The style_array of this StyleConfiguration.
        :rtype: List[StyleConfigurationStyleArray]
        """
        return self._style_array

    @style_array.setter
    def style_array(self, style_array: List[StyleConfigurationStyleArray]):
        """Sets the style_array of this StyleConfiguration.


        :param style_array: The style_array of this StyleConfiguration.
        :type style_array: List[StyleConfigurationStyleArray]
        """

        self._style_array = style_array

    @property
    def single_style(self) -> StyleConfigurationSingleStyle:
        """Gets the single_style of this StyleConfiguration.


        :return: The single_style of this StyleConfiguration.
        :rtype: StyleConfigurationSingleStyle
        """
        return self._single_style

    @single_style.setter
    def single_style(self, single_style: StyleConfigurationSingleStyle):
        """Sets the single_style of this StyleConfiguration.


        :param single_style: The single_style of this StyleConfiguration.
        :type single_style: StyleConfigurationSingleStyle
        """

        self._single_style = single_style
