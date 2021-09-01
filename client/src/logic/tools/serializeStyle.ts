import type { Style, StyleConfiguration } from "../../api";
import { stepSize } from "./stepsize";

function serializeSingleStyle(
  style: NonNullable<StyleConfiguration["singleStyle"]>
) {
  return `s-${style.id}-${style.layer}`;
}

function serializeStyleArray(
  styleArray: NonNullable<StyleConfiguration["styleArray"]>
) {
  let styleString = `a`;
  for (const style of styleArray) {
    styleString += `-${style.style1}`;
    if (style.style2 !== undefined && style.proportionStyle1 !== undefined) {
      const step = Math.round(style.proportionStyle1 / stepSize());
      styleString += `_${style.style2}_${step}`;
    }
  }
  return styleString;
}

export function serializeStyle(style: Style): string {
  return `${style.generatorId}-${
    style.style.singleStyle
      ? serializeSingleStyle(style.style.singleStyle!)
      : serializeStyleArray(style.style.styleArray!)
  }`;
}
