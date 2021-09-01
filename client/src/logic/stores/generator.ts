import type { Generator } from "../../api";
import { Writable } from "../tools/customStore";

class GeneratorWritable extends Writable<
  (Generator & { computedLayerCount: number }) | undefined
> {
  private static transformGenerator(generator: Generator | undefined) {
    if (generator) {
      const result = {
        ...generator,
        computedLayerCount:
          generator.numberOfLayers - generator.settings.reduceNumberOfLayersBy,
      };
      return result;
    } else {
      return undefined;
    }
  }

  constructor(generator: Generator | undefined) {
    super(GeneratorWritable.transformGenerator(generator));
  }

  set(generator: Generator | undefined) {
    super.set(GeneratorWritable.transformGenerator(generator));
  }
}

export const activeGenerator = new GeneratorWritable(undefined);
