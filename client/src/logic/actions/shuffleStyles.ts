// shuffle styles
// -> generate all images/styles + ratings new

import type { GeneratorSettings } from "../../api";
import { displayedImages, displayedStyles } from "../stores/displayed";
import { activeGenerator } from "../stores/generator";
import { getGenerators } from "../stores/models";
import { ShuffleAction } from "./shuffleAction";

export class ShuffleStylesAction extends ShuffleAction<[GeneratorSettings]> {
  protected async beforeCollect(settings: GeneratorSettings) {
    const generatorsWritable = await getGenerators();
    const generator = activeGenerator.get();
    if (!generator) {
      throw new Error("No generator selected");
    } else {
      generator.settings = settings;
      activeGenerator.set(generator);
      generatorsWritable.set(generatorsWritable.get());
      this.shuffleImages();
      await this.shuffleStyles();
    }
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
