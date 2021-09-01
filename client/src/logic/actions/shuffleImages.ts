// shuffle images
// - style view
// -> generate all images + ratings new
// - result view
// -> generate all images/styles + ratings new

import { displayedImages, displayedStyles } from "../stores/displayed";
import { ShuffleAction } from "./shuffleAction";

export class ShuffleImagesAction extends ShuffleAction<[number] | []> {
  protected async beforeCollect(numberOfImages?: number) {
    this.shuffleImages(numberOfImages);
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
    const images = displayedImages.get();
    if (!images) {
      throw new Error("No images shown");
    } else {
      return {
        images,
        ratings: images,
      };
    }
  }
}
