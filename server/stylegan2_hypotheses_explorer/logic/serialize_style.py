from typing import List

from ..models import Generator as GeneratorModel
from ..models import (StyleConfiguration, StyleConfigurationSingleStyle,
                      StyleConfigurationStyleArray)


def serialize_single_style(style: StyleConfigurationSingleStyle) -> str:
    return f"s-{style.id}-{style.layer}"


def serialize_style_array(style_array: List[StyleConfigurationStyleArray], step_size: float) -> str:
    style_string = "a"
    for style in style_array:
        style_string += f"-{style.style1}"
        if style.style2 is not None and style.proportion_style1 is not None:
            style_string += f"""_{style.style2}_{round(style.proportion_style1 / step_size)}"""
    return style_string


def serialize_style(style: StyleConfiguration, generator: GeneratorModel) -> str:
    return f"""{generator.id}-{
        serialize_style_array(style.style_array, generator.step_size)
        if style.single_style is None else
        serialize_single_style(style.single_style)
    }"""
