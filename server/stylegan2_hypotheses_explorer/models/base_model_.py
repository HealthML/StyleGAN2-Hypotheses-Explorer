import pprint
import typing

import six

from ..util import deserialize_model

T = typing.TypeVar('T')


class Base_Model(object):
    # swaggerTypes: The key is attribute name and the
    # value is attribute type.
    swagger_types = {}

    # attributeMap: The key is attribute name and the
    # value is json key in definition.
    attribute_map = {}

    @classmethod
    def from_dict(cls: typing.Type[T], dikt) -> T:
        """Returns the dict as a model"""
        return deserialize_model(dikt, cls)

    def to_dict(self):
        """Returns the model properties as a dict with correct object names"""
        def val_to_dict(val):
            if hasattr(val, "to_dict"):
                return val.to_dict()
            elif isinstance(val, list):
                return list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    val
                ))
            else:
                return val

        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[self.attribute_map[attr]] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[self.attribute_map[attr]] = value.to_dict()
            elif isinstance(value, dict):
                result[self.attribute_map[attr]] = dict(map(
                    lambda item: (item[0], val_to_dict(item[1])),
                    value.items()
                ))
            else:
                result[self.attribute_map[attr]] = value

        return result

    def to_str(self):
        """Returns the string representation of the model

        :rtype: str
        """
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
