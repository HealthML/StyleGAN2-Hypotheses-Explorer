// change view
// -> load all styles + ratings new (warning! before collect is called)

import { view, View } from "../stores/view";
import { displayedStyles } from "../stores/displayed";
import { Action, Changes } from "./action";
import { selectedImage } from "../stores/selectedImage";
import { copyStyle } from "../tools/copyStyle";
import { activeGenerator } from "../stores/generator";

export class ChangeViewAction extends Action<[View]> {
  protected async beforeCollect(selectedView: View) {
    view.set(selectedView);
  }

  protected async collectChangesResultView(): ReturnType<
    Action["collectChangesResultView"]
  > {
    const image = selectedImage.get();
    const styles = displayedStyles.get();
    if (!styles) {
      throw new Error("No styles shown");
    } else if (!image) {
      throw new Error("No image selected");
    } else {
      const imageStyle = image.style;
      const changes: Changes = {
        images: [],
        ratings: [],
      };
      for (let layer = 0; layer < styles.length; layer++) {
        for (const style of styles[layer]) {
          style.style = copyStyle(imageStyle);
          style.style.style.styleArray![layer] = {
            style1: style.id,
          };
          changes.images.push(style);
          changes.ratings.push(style);
        }
      }
      return changes;
    }
  }

  protected async collectChangesStyleView(): ReturnType<
    Action["collectChangesStyleView"]
  > {
    const styles = displayedStyles.get();
    const generator = activeGenerator.get();
    if (!generator) {
      throw new Error("No generator selected");
    } else if (!styles) {
      throw new Error("No styles shown");
    } else {
      const changes: Changes = {
        images: [],
        ratings: [],
      };
      for (let layer = 0; layer < styles.length; layer++) {
        for (const style of styles[layer]) {
          style.style = {
            generatorId: generator.id,
            style: {
              singleStyle: {
                layer,
                id: style.id,
              },
            },
          };

          changes.images.push(style);
          changes.ratings.push(style);
        }
      }
      return changes;
    }
  }
}
