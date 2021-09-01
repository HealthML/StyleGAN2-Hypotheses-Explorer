// switch image
// - style view
// -> nothing (only local update)
// - result view
// -> generate all styles + ratings new

import { displayedStyles, SpriteMapImage } from "../stores/displayed";
import { activeGenerator } from "../stores/generator";
import { selectedImage } from "../stores/selectedImage";
import { copyStyle } from "../tools/copyStyle";
import { Action } from "./action";

export class SwitchImageAction extends Action<[SpriteMapImage]> {
  private makeImageStyleDisplayable(image: SpriteMapImage) {
    const generator = activeGenerator.get();
    const styles = displayedStyles.get();
    const imageStyle = image.style.style.styleArray;
    if (!generator) {
      throw new Error("No generator selected");
    } else if (!imageStyle) {
      throw new Error("Image has invalid or non existing style");
    } else {
      let changes: boolean = false;
      for (let layer = 0; layer < generator.computedLayerCount; layer++) {
        const layerStyles = styles[layer];
        const layerImageStyle = imageStyle[layer];
        const style1Index = layerStyles.findIndex(
          (style) => style.id === layerImageStyle.style1
        );
        const style2Index = layerStyles.findIndex(
          (style) => style.id === layerImageStyle.style2
        );
        if (style1Index === -1 || style1Index === style2Index) {
          throw new Error("Image uses invalid style");
        } else {
          if (style2Index >= 0) {
            let upperIndex = Math.max(style1Index, style2Index);
            let lowerIndex = Math.min(style1Index, style2Index);
            if (upperIndex - lowerIndex > 1) {
              const [movingStyle] = layerStyles.splice(upperIndex, 1);
              layerStyles.splice(lowerIndex + 1, 0, movingStyle);
              changes = true;
            }
          }
        }
      }
      if (changes) {
        displayedStyles.set(styles);
      }
    }
  }

  protected async beforeCollect(image: SpriteMapImage) {
    this.makeImageStyleDisplayable(image);
    selectedImage.set(image);
  }

  protected async collectChangesResultView(
    image: SpriteMapImage
  ): ReturnType<Action["collectChangesResultView"]> {
    const generator = activeGenerator.get();
    const styles = displayedStyles.get();

    if (!generator) {
      throw new Error("No generator selected");
    } else if (!styles) {
      throw new Error("No styles shown");
    } else {
      const imageStyle = image.style;
      const changes = await this.collectChangesStyleView();

      for (let layer = 0; layer < generator.computedLayerCount; layer++) {
        for (const shownStyle of styles[layer]) {
          shownStyle.style = copyStyle(imageStyle);
          shownStyle.style.style.styleArray![layer] = {
            style1: shownStyle.id,
          };

          changes.images.push(shownStyle);
          changes.ratings.push(shownStyle);
        }
      }
      return changes;
    }
  }

  protected async collectChangesStyleView(): ReturnType<
    Action["collectChangesStyleView"]
  > {
    return {
      images: [],
      ratings: [],
    };
  }
}
