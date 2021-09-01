import { GeneratorApi, Style, StyleConfigurationStyleArray } from "../../api";
import { displayedImages, displayedStyles } from "../stores/displayed";
import { activeGenerator } from "../stores/generator";
import { selectedImage } from "../stores/selectedImage";
import { View, view } from "../stores/view";
import { BlobURLFake } from "../tools/blobURL";
import { copyStyle } from "../tools/copyStyle";
import { randint } from "../tools/randint";
import { Action } from "./action";

export abstract class ShuffleAction<
  ArgsTypes extends Array<any> = []
> extends Action<ArgsTypes> {
  protected shuffleImages(numberOfImages?: number) {
    if (!numberOfImages) {
      const images = displayedImages.get();
      if (!images) {
        throw new Error("No images shown");
      } else {
        numberOfImages = images.length;
      }
    }
    const generator = activeGenerator.get();
    const images = displayedImages.get();

    if (!generator) {
      throw new Error("No generator selected");
    } else if (!images) {
      throw new Error("No images shown");
    } else {
      const stylesPerLayer = generator.settings.numGenStylesPerLayer;

      for (const image of images) {
        image.src.decreaseUses();
      }
      images.length = 0;

      for (let index = 0; index < numberOfImages; index++) {
        const styleArray: StyleConfigurationStyleArray[] = [];
        for (let layer = 0; layer < generator.computedLayerCount; layer++) {
          styleArray.push({
            style1: randint(0, stylesPerLayer),
            style2: randint(0, stylesPerLayer),
            proportionStyle1: Math.random(),
          });
        }

        images.push({
          container: displayedImages,
          height: 256,
          offsetX: 0,
          rating: 0,
          width: 256,
          src: new BlobURLFake(),
          style: {
            generatorId: generator.id,
            style: {
              styleArray,
            },
          },
        });
      }
      selectedImage.set(images[0]);
    }
  }

  protected createStylesForCurrentSettings() {
    const generator = activeGenerator.get();
    const styles = displayedStyles.get();
    const currentView = view.get();
    const image = selectedImage.get();
    if (!generator) {
      throw new Error("No generator selected");
    } else if (!styles) {
      throw new Error("No styles shown");
    } else {
      for (const style of styles.flat()) {
        style.src.decreaseUses();
      }
      styles.length = 0;
      for (let layer = 0; layer < generator.computedLayerCount; layer++) {
        const styleIds = [];
        for (
          let style = 0;
          style < generator.settings.numGenStylesPerLayer;
          style++
        ) {
          styleIds.push(style);
        }
        styles.push(
          styleIds.map((styleId) => {
            let style: Style = {
              generatorId: generator!.id,
              style: {
                singleStyle: {
                  layer,
                  id: styleId,
                },
              },
            };
            if (currentView === View.STYLE_VIEW) {
            } else if (currentView === View.RESULT_VIEW) {
              if (!image) {
                throw new Error("No image selected.");
              } else {
                style = copyStyle(image.style);
                style.style.styleArray![layer] = {
                  style1: styleId,
                };
              }
            } else {
              throw new Error("Unknown view encountered.");
            }
            return {
              id: styleId,
              container: displayedStyles,
              height: 256,
              offsetX: 0,
              rating: 0,
              width: 256,
              src: new BlobURLFake(),
              style,
              loading: true,
            };
          })
        );
      }
      displayedStyles.set(styles);
    }
  }

  protected async shuffleStyles() {
    const generator = activeGenerator.get();
    const styles = displayedStyles.get();
    if (!generator) {
      throw new Error("No generator selected");
    } else if (!styles) {
      throw new Error("No styles shown");
    } else {
      this.createStylesForCurrentSettings();
      await new GeneratorApi().generatorGeneratorIdGenerateNewStylesPut(
        generator.settings,
        generator.id
      );
    }
  }
}
