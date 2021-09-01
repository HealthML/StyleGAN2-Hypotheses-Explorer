// select generator
// -> generate all images/styles + ratings new

import type { Generator } from "../../api";
import { displayedImages, displayedStyles } from "../stores/displayed";
import { activeGenerator } from "../stores/generator";
import { ShuffleAction } from "./shuffleAction";

export class SelectGeneratorAction extends ShuffleAction<[Generator]> {
  protected async beforeCollect(generator: Generator) {
    activeGenerator.set(generator);
    this.shuffleImages(parseInt(process.env.default_num_gen_images!));
    this.createStylesForCurrentSettings();
  }

  protected async collectChangesResultView(): ReturnType<
    ShuffleAction["collectChangesResultView"]
  > {
    const styles = displayedStyles.get();
    const images = displayedImages.get();
    if (!styles) {
      throw new Error("No styles shown");
    } else if (!images) {
      throw new Error("No images shown");
    } else {
      const allStylesAndImages = [styles.flat(), images].flat();
      return {
        images: allStylesAndImages,
        ratings: allStylesAndImages,
      };
    }
  }

  protected async collectChangesStyleView(): ReturnType<
    ShuffleAction["collectChangesStyleView"]
  > {
    return this.collectChangesResultView();
  }
}
