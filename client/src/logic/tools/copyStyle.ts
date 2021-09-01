import type { Style } from "../../api";

export function copyStyle(style: Style): Style {
  return {
    generatorId: style.generatorId,
    style: style.style.singleStyle
      ? { singleStyle: { ...style.style.singleStyle } }
      : {
          styleArray: style.style.styleArray!.map((mixedStyleInLayer) => {
            return { ...mixedStyleInLayer };
          }),
        },
  };
}
