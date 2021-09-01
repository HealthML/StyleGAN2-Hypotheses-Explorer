import type { Style } from "../../api";
import { normalizeStyle } from "./nomalizeStyles";

export type StyleArrayElement = NonNullable<Style["style"]["styleArray"]>[0];

export function stylesEqual(
  style1: StyleArrayElement,
  style2: StyleArrayElement
) {
  style1 = { ...style1 };
  style2 = { ...style2 };
  normalizeStyle(style1);
  normalizeStyle(style2);
  return (
    style1.proportionStyle1 === style2.proportionStyle1 &&
    style1.style1 === style2.style1 &&
    style1.style2 === style2.style2
  );
}
