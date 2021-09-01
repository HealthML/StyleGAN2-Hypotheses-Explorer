import type { Style } from "../../api";
import { roundToStepSize } from "./stepsize";
import type { StyleArrayElement } from "./styleArrayElement";

function normalizeProportion(style: StyleArrayElement) {
  if (style.proportionStyle1) {
    style.proportionStyle1 = roundToStepSize(style.proportionStyle1);
  }
}

function isSingleStyle(style: StyleArrayElement) {
  return (
    style.proportionStyle1 === 0 ||
    style.proportionStyle1 === 1 ||
    style.style2 === undefined ||
    style.proportionStyle1 === undefined ||
    style.style1 === style.style2
  );
}

function normalizeOrder(style: StyleArrayElement) {
  if (style.style2! > style.style1) {
    const style1 = style.style1;
    style.style1 = style.style2!;
    style.style2 = style1;
    style.proportionStyle1 = 1 - style.proportionStyle1!;
  }
}

export function normalizeStyle(style: StyleArrayElement) {
  normalizeProportion(style);
  if (isSingleStyle(style)) {
    if (style.proportionStyle1 === 0) {
      style.style1 = style.style2!;
    }
    delete style.proportionStyle1;
    delete style.style2;
  } else {
    normalizeOrder(style);
  }
}

export function normalizeStyles(styles: Style[]): Style[] {
  for (const style of styles) {
    if (style.style.styleArray) {
      for (const styleConfigurationInLayer of style.style.styleArray) {
        normalizeStyle(styleConfigurationInLayer);
      }
    }
  }
  return styles;
}
