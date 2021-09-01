import { EvaluatorApi, GeneratorApi, Style } from "../api";
import type { SpriteMapPart } from "./stores/displayed";
import { activeEvaluator } from "./stores/evaluator";
import { activeGenerator } from "./stores/generator";
import { createBlobURL } from "./tools/blobURL";
import { getImageDimensions } from "./tools/imageDimensions";
import { normalizeStyles } from "./tools/nomalizeStyles";
import { serializeStyle } from "./tools/serializeStyle";

export async function fetchRatings(styles: Style[]): Promise<number[]> {
  if (styles.length > 0) {
    const evaluator = activeEvaluator.get();
    const generator = activeGenerator.get();
    if (!evaluator) {
      throw new Error("No evaluator selected");
    } else if (!generator) {
      throw new Error("No generator selected");
    } else {
      styles = normalizeStyles(styles);
      if (generator.offlineMode) {
        return Promise.all(
          styles.map((style) =>
            new EvaluatorApi().evaluatorEvaluatorIdEvaluateStyleGet(
              evaluator.id,
              serializeStyle(style)
            )
          )
        );
      } else {
        return new EvaluatorApi().evaluatorEvaluatorIdEvaluatePost(
          {
            generatorId: generator.id,
            styles: styles.map((style) => style.style),
          },
          evaluator.id
        );
      }
    }
  } else {
    return [];
  }
}

export async function fetchImages(styles: Style[]): Promise<SpriteMapPart[]> {
  if (styles.length > 0) {
    const generator = activeGenerator.get();
    if (!generator) {
      throw new Error("No generator selected");
    } else {
      styles = normalizeStyles(styles);
      if (generator.offlineMode) {
        return Promise.all(
          styles.map((style) =>
            new GeneratorApi()
              .generatorGenerateStyleGet(serializeStyle(style))
              .then(createBlobURL)
              .then(async (src) => {
                src.increaseUses();
                return {
                  src,
                  offsetX: 0,
                  ...(await getImageDimensions(src.url)),
                };
              })
          )
        );
      } else {
        return new GeneratorApi()
          .generatorGeneratorIdGeneratePost(
            styles.map((style) => style.style),
            generator.id
          )
          .then(createBlobURL)
          .then(async (src) => {
            const { height } = await getImageDimensions(src.url);
            const sharedSpriteMapPartProperties = {
              height,
              width: height,
              src,
            };
            src.increaseUses(styles.length);
            return styles.map((_, index) => {
              return {
                ...sharedSpriteMapPartProperties,
                offsetX: index * height,
              };
            });
          });
      }
    }
  } else {
    return [];
  }
}
