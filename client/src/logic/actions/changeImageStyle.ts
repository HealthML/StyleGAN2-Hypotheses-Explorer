// change image style
// - style view
// -> generate single image + rating new
// - result view
// -> generate single image/all styles except for changed column + ratings new

import { activeGenerator } from "../stores/generator";
import { selectedImage } from "../stores/selectedImage";
import { copyStyle } from "../tools/copyStyle";
import { displayedStyles } from "../stores/displayed";
import { Action } from "./action";

export class ChangeImageStyleAction extends Action<[number]> {
  protected async collectChangesResultView(
    changed_layer: number
  ): ReturnType<Action["collectChangesResultView"]> {
    const image = selectedImage.get();
    const generator = activeGenerator.get();
    const styles = displayedStyles.get();

    if (!generator) {
      throw new Error("No generator selected");
    } else if (!styles) {
      throw new Error("No styles shown");
    } else if (!image) {
      throw new Error("No image selected");
    } else {
      const imageStyle = image.style;
      const changes = await this.collectChangesStyleView();

      for (let layer = 0; layer < generator.computedLayerCount; layer++) {
        if (layer !== changed_layer) {
          for (const shownStyle of styles[layer]) {
            shownStyle.style = copyStyle(imageStyle);
            shownStyle.style.style.styleArray![layer] = {
              style1: shownStyle.id,
            };

            changes.images.push(shownStyle);
            changes.ratings.push(shownStyle);
          }
        }
      }
      return changes;
    }
  }

  protected async collectChangesStyleView(): ReturnType<
    Action["collectChangesStyleView"]
  > {
    const image = selectedImage.get();
    if (image) {
      return {
        images: [image],
        ratings: [image],
      };
    } else {
      throw new Error("No image selected");
    }
  }
}
